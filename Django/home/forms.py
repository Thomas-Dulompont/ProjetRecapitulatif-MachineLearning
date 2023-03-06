from django import forms
from django.core.validators import MinValueValidator

class ApiForm(forms.Form):
    Name = forms.CharField(max_length=250)