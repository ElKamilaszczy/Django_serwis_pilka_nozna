from django import forms
from .models import Liga, Klub, Pilkarz, Mecz, Statystyki_gracza

class LigaForm(forms.ModelForm):
    class Meta:
        model = Liga
        fields = ('nazwa_ligi',)

class KlubForm(forms.ModelForm):
    class Meta:
        model = Klub
        fields = ('nazwa_klubu', 'id_ligi',)
#Formularz logowania dla organizatorów
class LoginForm(forms.Form):
    login = forms.CharField()
    hasło = forms.CharField(widget=forms.PasswordInput)