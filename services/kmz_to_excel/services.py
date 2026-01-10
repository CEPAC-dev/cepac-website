import os
from django.conf import settings
from .utils import convert_kmz_to_excel

def handle_kmz_to_excel(uploaded_file, base_name):
    uploads_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    converted_dir = os.path.join(settings.MEDIA_ROOT, "converted")
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(converted_dir, exist_ok=True)

    input_kmz_path = os.path.join(uploads_dir, f"{base_name}.kmz")
    with open(input_kmz_path, "wb+") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    output_excel_path = os.path.join(converted_dir, f"{base_name}.xlsx")
    convert_kmz_to_excel(input_kmz_path, output_excel_path)

    return output_excel_path
