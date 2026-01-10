import os
import tempfile
from django.conf import settings
from .utils import extract_kml_from_kmz, build_shapefile_archive

def handle_kmz_to_shapefile(uploaded_file, base_name):
    uploads_dir   = os.path.join(settings.MEDIA_ROOT, "uploads")
    converted_dir = os.path.join(settings.MEDIA_ROOT, "converted")
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(converted_dir, exist_ok=True)

    input_kmz_path = os.path.join(uploads_dir, f"{base_name}.kmz")
    with open(input_kmz_path, "wb+") as dst:
        for chunk in uploaded_file.chunks():
            dst.write(chunk)

    tmp_folder = os.path.join(uploads_dir, f"tmp_{base_name}")
    kml_path   = extract_kml_from_kmz(input_kmz_path, tmp_folder)

    output_zip = os.path.join(converted_dir, f"{base_name}.zip")
    build_shapefile_archive(kml_path, output_zip)

    return output_zip
