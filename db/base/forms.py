from django import forms
from django.forms import ModelForm

from db.base.models import Transponder


class SatelliteSearchForm(forms.Form):
    term = forms.CharField()


class TransponderSuggestionForm(forms.ModelForm):
    class Meta:
        model = Transponder
        exclude = ['approved']
