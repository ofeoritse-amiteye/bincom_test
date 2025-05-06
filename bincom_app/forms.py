from django import forms
from .models import AnnouncedPuResults

class ResultForm(forms.ModelForm):
    class Meta:
        model = AnnouncedPuResults
        fields = ['polling_unit_uniqueid', 'party_abbreviation', 'party_score', 'entered_by_user',]