import os
from django.conf import settings
from .utils import analyze_and_repackage

def handle_kmz_polygon_analysis(uploaded_file, base_name):
    """
    Saves uploaded file, processes it, returns paths to results.
    """
    uploads_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    converted_dir = os.path.join(settings.MEDIA_ROOT, "converted")
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(converted_dir, exist_ok=True)

    input_kmz_filename = f"{base_name}.kmz"
    input_kmz_path = os.path.join(uploads_dir, input_kmz_filename)
    with open(input_kmz_path, "wb+") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    output_kmz = os.path.join(converted_dir, f"{base_name}_updated.kmz")
    output_excel = os.path.join(converted_dir, f"{base_name}_summary.xlsx")

    analyze_and_repackage(input_kmz_path, output_kmz, output_excel)

    return output_kmz, output_excel
