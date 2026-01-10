import os
import json
import subprocess
import uuid
from typing import List, Tuple, Optional
from django.conf import settings

def get_session_directory(session_id: str) -> str:
    """Get or create a session-specific directory"""
    session_dir = os.path.join(settings.MEDIA_ROOT, "TLD", f"session_{session_id}")
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

def build_time_edges(minimum: float, maximum: float, intervals: int) -> Tuple[float, List[float]]:
    """
    Create edges like [min+step, min+2*step, ..., max] (length == intervals).
    Returns (step, edges_list).
    """
    if intervals <= 0:
        raise ValueError("intervals must be > 0")
    if maximum <= minimum:
        raise ValueError("maximum must be > minimum")

    step = (maximum - minimum) / intervals
    times: List[float] = []
    cur = minimum
    for _ in range(intervals):
        cur += step
        times.append(cur)
    return step, times

def normalize_frequencies(freqs: List[float]) -> List[float]:
    """Normalize so they sum to 1.0 (raises if sum <= 0)."""
    s = sum(freqs)
    if s <= 0:
        raise ValueError("Sum of frequencies must be > 0.")
    return [f / s for f in freqs]

def save_matrix_to_media(array_of_time: List[float], normalized: List[float], session_id: str) -> str:
    """
    Save [[time_i, norm_i], ...] as session-specific JSON for Octave to read.
    Returns the file path.
    """
    session_dir = get_session_directory(session_id)
    matrix = [[array_of_time[i], normalized[i]] for i in range(len(array_of_time))]
    out = os.path.join(session_dir, "tld_data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(matrix, f)
    return out

def _find_octave_exe() -> str:
    """
    Try a few common Octave paths on Windows; fallback to 'octave' on PATH.
    """
    candidates = [
        r"C:\Program Files\GNU Octave\Octave-10.3.0\octave-launch.exe",
        
        
    ]
    for c in candidates:
        if os.path.isabs(c):
            if os.path.exists(c):
                return c
        else:
            return c
    return "octave"

def run_octave_script(session_id: str) -> None:
    """
    Run the Octave script with session-specific paths
    """
    session_dir = get_session_directory(session_id)
    input_path = os.path.join(session_dir, "tld_data.json")
    
    script_dir = os.path.join(
        settings.BASE_DIR,
        "services", "trip_length_distribution", "static", "tld"
    )
    script_name = "Combined_TLD_Function_21_2_2024.m"
    script_path = os.path.join(script_dir, script_name)
    
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Octave script not found at: {script_path}")

    # Prepare paths with forward slashes for Octave
    safe_input_path = input_path.replace("\\", "/")
    safe_session_dir = session_dir.replace("\\", "/")
    
    # Call the function with our custom paths
    eval_str = f"cd('{script_dir}'); Combined_TLD_Function_21_2_2024('{safe_input_path}', '{safe_session_dir}')"

    octave_path = _find_octave_exe()
    cmd = [octave_path, "--no-gui", "--eval", eval_str]

    result = subprocess.run(
        cmd,
        cwd=script_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Octave failed (code {}).\nSTDOUT:\n{}\nSTDERR:\n{}\n".format(
                result.returncode, result.stdout, result.stderr
            )
        )

def load_fitting_results(session_id: str) -> Optional[dict]:
    """Read session-specific fitting_results.json, return dict or None if missing."""
    session_dir = get_session_directory(session_id)
    json_path = os.path.join(session_dir, "fitting_results.json")
    if not os.path.exists(json_path):
        return None
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_plot_url(session_id: str) -> str:
    """Get the URL for the session-specific plot"""
    session_dir_name = f"session_{session_id}"
    return f"{settings.MEDIA_URL}TLD/{session_dir_name}/Fitting_Results.png"

def cleanup_session_data(session_id: str) -> None:
    """Clean up session-specific files"""
    session_dir = get_session_directory(session_id)
    try:
        import shutil
        shutil.rmtree(session_dir)
    except Exception as e:
        print(f"Error cleaning up session data: {e}")