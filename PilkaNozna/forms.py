from django import forms
from .models import Liga

class PostForm(forms.ModelForm):
    class Meta:
        model = Liga
        fields = ('nazwa_ligi',)

#Formularz logowania dla organizatorów
class LoginForm(forms.Form):
    login = forms.CharField()
    hasło = forms.CharField(widget=forms.PasswordInput)