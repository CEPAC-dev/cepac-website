import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify
from .forms import KMZUploadForm
from .services import handle_kmz_polygon_analysis
from django.contrib.auth.decorators import login_required
@login_required
def form_view(request):
    if request.method == "POST":
        form = KMZUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            if not uploaded.name.lower().endswith(".kmz"):
                messages.error(request, "Please upload a .kmz file.")
                return redirect(reverse("kmz_polygon_analysis:form"))

            base_name = slugify(os.path.splitext(uploaded.name)[0])
            try:
                output_kmz, output_excel = handle_kmz_polygon_analysis(uploaded, base_name)
                return render(request, "kmz_polygon_analysis/success.html", {
                    "kmz_link": f"/media/converted/{os.path.basename(output_kmz)}",
                    "excel_link": f"/media/converted/{os.path.basename(output_excel)}",
                })
            except Exception as e:
                messages.error(request, f"Processing failed: {e}")
                return redirect(reverse("kmz_polygon_analysis:form"))
    else:
        form = KMZUploadForm()
    return render(request, "kmz_polygon_analysis/form.html", {"form": form})
