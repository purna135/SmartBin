from django import forms
from .models import Bin

class BinsForm(forms.ModelForm):

    class Meta:
        model = Bin
        fields = ["name", "height", "location", "longitude", "latitude"]