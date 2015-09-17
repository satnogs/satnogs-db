from django import forms

from db.base.models import Suggestion


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ['user', 'uuid']
