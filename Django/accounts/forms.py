from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserFormCustom(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserFormCustom, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Nom..'})
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Email..'})
        self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Mot de passe..'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Confirmer mot de passe..'})