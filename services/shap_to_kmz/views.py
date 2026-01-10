# services/shap_to_kmz/views.py

import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify

from .forms import ShapToKmzForm
from .services import handle_shap_to_kmz
from django.contrib.auth.decorators import login_required
@login_required 
def form_view(request):
    if request.method == "POST":
        form = ShapToKmzForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            # strip extension and slugify
            base_name = slugify(uploaded.name.rsplit(".", 1)[0])
            try:
                # this returns the full filesystem path
                output_kml_path = handle_shap_to_kmz(uploaded, base_name)
                # get just the filename
                filename = os.path.basename(output_kml_path)
                # build a media URL pointing at /media/converted/<filename>
                download_url = settings.MEDIA_URL + "converted/" + filename

                return render(request, "shap_to_kmz/success.html", {
                    "download_link": download_url,
                    "filename":      filename,
                })
            except Exception as e:
                messages.error(request, f"Conversion failed: {e}")
                return redirect(reverse("shap_to_kmz:form"))
    else:
        form = ShapToKmzForm()

    return render(request, "shap_to_kmz/form.html", {"form": form})
