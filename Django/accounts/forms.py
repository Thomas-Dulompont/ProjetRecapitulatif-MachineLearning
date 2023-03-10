from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class UserFormCustom(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserFormCustom, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Nom..'})
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email..'})
        self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Mot de passe..'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Confirmer mot de passe..'})


class MusicSearchForm(forms.Form):
    music_name = forms.CharField(label="Nom de musique", max_length=256, required=False)
    artist_name = forms.CharField(label="Artiste", max_length=256, required=False)
    
    def __init__(self, *args, **kwargs):
       super(MusicSearchForm, self).__init__(*args, **kwargs)
       self.fields['music_name'].widget.attrs.update({'class':'form-control', 'placeholder':"Entrez le nom de la musique"})
       self.fields['artist_name'].widget.attrs.update({'class':'form-control','placeholder':"Entrez le nom de l'artiste"})