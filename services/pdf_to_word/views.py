import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import PdfToWordForm
from .services import handle_pdf_to_word
@login_required
def form_view(request):
    if request.method == "POST":
        form = PdfToWordForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            if not uploaded.name.lower().endswith(".pdf"):
                messages.error(request, "Only PDF files are allowed.")
                return redirect(reverse("pdf_to_word:form"))

            base_name = slugify(os.path.splitext(uploaded.name)[0])
            try:
                output_docx = handle_pdf_to_word(uploaded, base_name)
                return render(request, "pdf_to_word/success.html", {
                    "download_link": f"/media/converted/{os.path.basename(output_docx)}",
                    "filename": os.path.basename(output_docx),
                })
            except Exception as e:
                messages.error(request, f"Conversion failed: {e}")
                return redirect(reverse("pdf_to_word:form"))
    else:
        form = PdfToWordForm()
    return render(request, "pdf_to_word/form.html", {"form": form})
