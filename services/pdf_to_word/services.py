import os
from django.conf import settings
from pdf2docx import Converter
from .utils import allowed_file

def handle_pdf_to_word(uploaded_file, base_name):
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    converted_dir = os.path.join(settings.MEDIA_ROOT, "converted")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(converted_dir, exist_ok=True)

    pdf_filename = f"{base_name}.pdf"
    docx_filename = f"{base_name}.docx"

    pdf_path = os.path.join(upload_dir, pdf_filename)
    docx_path = os.path.join(converted_dir, docx_filename)

    # Save uploaded PDF
    with open(pdf_path, "wb+") as dest:
        for chunk in uploaded_file.chunks():
            dest.write(chunk)

    if not allowed_file(pdf_filename):
        raise ValueError("Only .pdf files are supported.")

    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
    except Exception as e:
        # Clean up partially written output if any
        if os.path.exists(docx_path):
            os.remove(docx_path)
        raise RuntimeError(f"Conversion failed: {e}")

    return docx_path
