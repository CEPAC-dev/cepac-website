from django import forms

class KMZToShapefileForm(forms.Form):
    file = forms.FileField(
        label="KMZ File",
        help_text="Upload a .kmz file to convert into shapefile(s) (.zip archive).",
        widget=forms.ClearableFileInput(attrs={"accept": ".kmz"})
    )
