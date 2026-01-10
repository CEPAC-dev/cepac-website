from django import forms

class ShapToKmzForm(forms.Form):
    file = forms.FileField(
        label="Shapefile Archive",
        help_text="Upload a .zip or .rar containing the shapefile components (.shp, .shx, .dbf etc.).",
        widget=forms.ClearableFileInput(attrs={"accept": ".zip,.rar"})
    )
