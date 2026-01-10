import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import KMZToShapefileForm
from .services import handle_kmz_to_shapefile
@login_required
def form_view(request):
    if request.method == "POST":
        form = KMZToShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            if not uploaded.name.lower().endswith(".kmz"):
                messages.error(request, "Please upload a .kmz file.")
                return redirect(reverse("kmz_to_shapefile:form"))

            base_name = slugify(os.path.splitext(uploaded.name)[0])
            try:
                output_zip = handle_kmz_to_shapefile(uploaded, base_name)
                filename   = os.path.basename(output_zip)
                download   = settings.MEDIA_URL + "converted/" + filename
                return render(request, "kmz_to_shapefile/success.html", {
                    "download_link": download,
                    "filename":      filename,
                })
            except Exception as e:
                messages.error(request, f"Conversion failed: {e}")
                return redirect(reverse("kmz_to_shapefile:form"))
    else:
        form = KMZToShapefileForm()

    return render(request, "kmz_to_shapefile/form.html", {"form": form})
