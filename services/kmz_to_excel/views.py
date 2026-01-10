import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify
from .forms import KMZToExcelForm
from .services import handle_kmz_to_excel
from django.contrib.auth.decorators import login_required
@login_required
def form_view(request):
    if request.method == "POST":
        form = KMZToExcelForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            if not uploaded.name.lower().endswith(".kmz"):
                messages.error(request, "Please upload a .kmz file.")
                return redirect(reverse("kmz_to_excel:form"))

            base_name = slugify(os.path.splitext(uploaded.name)[0])
            try:
                output_excel = handle_kmz_to_excel(uploaded, base_name)
                return render(request, "kmz_to_excel/success.html", {
                    "download_link": f"/media/converted/{os.path.basename(output_excel)}",
                    "filename": os.path.basename(output_excel),
                })
            except Exception as e:
                messages.error(request, f"Conversion failed: {e}")
                return redirect(reverse("kmz_to_excel:form"))
    else:
        form = KMZToExcelForm()
    return render(request, "kmz_to_excel/form.html", {"form": form})
