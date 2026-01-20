from django import forms
from .models import Club, Player, Opposition


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'home_ground', 'default_match_fee']

class PlayerForm(forms.ModelForm):
    """Form for creating and editing players"""
    class Meta:
        model = Player
        fields = ['name', 'email', 'phone']

class OppositionForm(forms.ModelForm):
    """Form for creating and editing opposition teams"""
    class Meta:
        model = Opposition
        fields = ['name', 'home_ground']      