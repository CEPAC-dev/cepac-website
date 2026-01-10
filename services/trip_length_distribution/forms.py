from django import forms

class TripLengthForm(forms.Form):
    Minimum = forms.CharField(
        label="Minimum of TLD",
        widget=forms.TextInput(attrs={"style": "width:250px;", "id": "Minimum"})
    )
    Maximum = forms.CharField(
        label="Maximum of TLD",
        widget=forms.TextInput(attrs={"style": "width:250px;", "id": "Maximum"})
    )
    intervals = forms.IntegerField(
        min_value=1,
        max_value=300,
        label="Number of Intervals",
        widget=forms.NumberInput(attrs={"style": "width:250px;", "id": "intervals"})
    )
