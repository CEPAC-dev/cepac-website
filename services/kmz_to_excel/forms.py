from django import forms

class KMZToExcelForm(forms.Form):
    file = forms.FileField(
        label="KMZ File",
        help_text="Upload a .kmz file to extract polygon/geometry data into Excel.",
        widget=forms.ClearableFileInput(attrs={"accept": ".kmz"})
    )
