from django import forms

class PdfToWordForm(forms.Form):
    file = forms.FileField(
        label="PDF File",
        help_text="Upload a PDF file to convert to DOCX.",
        widget=forms.ClearableFileInput(attrs={"accept": ".pdf"})
    )
