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

class MeczForm(forms.ModelForm):
    class Meta:
        model = Mecz
        fields = ('id_klubu1', 'id_klubu2', 'kolejka', 'data_meczu',)
        widgets = {
            'data_meczu' : forms.DateInput(attrs={'type': 'date'}),
            'kolejka': forms.NumberInput(),
        }
class StatystykiForm(forms.ModelForm):
    class Meta:
        model = Statystyki_gracza
        fields = ('id_pilkarza', 'id_meczu', 'gole', 'asysty', 'faule', 'zolta', 'czerwona',)
#Formularz logowania dla organizatorów
class LoginForm(forms.Form):
    login = forms.CharField()
    hasło = forms.CharField(widget=forms.PasswordInput)