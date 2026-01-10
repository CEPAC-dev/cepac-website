import os
import shutil
import uuid
from django.utils.text import slugify
from django.conf import settings

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def unique_filename(original_name):
    base, ext = os.path.splitext(original_name)
    safe_base = slugify(base)
    unique_suffix = uuid.uuid4().hex[:8]
    return f"{safe_base}_{unique_suffix}{ext}"

def save_upload(file_obj, target_dir, allow_overwrite=False):
    """
    Saves uploaded Django InMemoryUploadedFile or TemporaryUploadedFile to target_dir.
    Returns the absolute path to saved file.
    """
    ensure_dir(target_dir)
    filename = file_obj.name
    if not allow_overwrite:
        filename = unique_filename(filename)
    destination_path = os.path.join(target_dir, filename)
    with open(destination_path, "wb+") as dest:
        for chunk in file_obj.chunks():
            dest.write(chunk)
    return destination_path

def remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    elif os.path.isfile(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

def clean_old_files(directory, keep_last_n=5):
    """
    Optionally cleans up old files, keeping the newest `keep_last_n`.
    """
    if not os.path.isdir(directory):
        return
    entries = sorted(
        (os.path.join(directory, f) for f in os.listdir(directory)),
        key=lambda p: os.path.getmtime(p),
        reverse=True,
    )
    for old in entries[keep_last_n:]:
        remove_path(old)
