from django import forms

from db.base.models import Suggestion


class SatelliteSearchForm(forms.Form):
    term = forms.CharField()


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ['user']
