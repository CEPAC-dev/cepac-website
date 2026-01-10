import os
import tempfile
import zipfile
import rarfile

def extract_compressed_file(input_path, extract_to):
    if input_path.lower().endswith(".zip"):
        with zipfile.ZipFile(input_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
    elif input_path.lower().endswith(".rar"):
        with rarfile.RarFile(input_path, "r") as rar_ref:
            rar_ref.extractall(extract_to)
    else:
        raise ValueError("Unsupported archive format. Only .zip or .rar allowed.")

def allowed_file(filename):
    return filename.lower().endswith((".zip", ".rar"))
