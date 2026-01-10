from django import forms

class KMZUploadForm(forms.Form):
    file = forms.FileField(
        label="KMZ File",
        help_text="Upload a .kmz file containing KML polygons.",
        widget=forms.ClearableFileInput(attrs={"accept": ".kmz"})
    )
