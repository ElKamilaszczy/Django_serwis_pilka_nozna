from django import forms
from .models import Liga, Klub, Pilkarz, Mecz, Statystyki_gracza
from django.core.validators import RegexValidator, MinValueValidator
import datetime
class LigaForm(forms.ModelForm):
    class Meta:
        model = Liga
        fields = ('nazwa_ligi',)

class KlubForm(forms.ModelForm):
    nazwa_klubu = forms.TextInput()
    class Meta:
        model = Klub
        fields = ('nazwa_klubu', 'id_ligi',)
    def clean_nazwa_klubu(self):
        klub = self.cleaned_data(['nazwa_klubu'])
        if klub != klub.capitalize():
            raise forms.ValidationError('Nazwa klubu musi rozpoczynać się od wielkiej litery.')
        return klub
'''
WALIDACJA:
- CZY KLUBY SĄ W TEJ SAMEJ LIDZE
'''
class MeczForm(forms.ModelForm):
    id_klubu1 = forms.TextInput()
    id_klubu2 = forms.TextInput()
    class Meta:
        model = Mecz
        fields = ('id_klubu1', 'id_klubu2', 'kolejka', 'data_meczu',)
        widgets = {
            'data_meczu' : forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_kolejka(self):
        kolejkaa = self.cleaned_data['kolejka']
        if kolejkaa <= 0:
            raise forms.ValidationError('Numer kolejki musi być większy od 0')
        return kolejkaa
    def clean_data_meczu(self):
        data = self.cleaned_data['data_meczu']
        if data > datetime.date.today():
            raise forms.ValidationError('Niepoprawna data! Podaj poprawna datę meczu.')
        return data
    def clean(self):
        id_klubuu1 = self.cleaned_data['id_klubu1']
        id_klubuu2 = self.cleaned_data['id_klubu2']
        kl1 = Klub.objects.get(nazwa_klubu = id_klubuu1)
        kl2 = Klub.objects.get(nazwa_klubu = id_klubuu2)
        if kl1.id_ligi != kl2.id_ligi:
            raise forms.ValidationError('Inne ligi drużyn')
        return id_klubuu1, id_klubuu2

#Zrobić
# - czy zawodnik jest w danym klubie
class StatystykiForm(forms.ModelForm):
    id_pilkarza = forms.NumberInput()
    id_meczu = forms.NumberInput()
    class Meta:
        model = Statystyki_gracza
        fields = ('id_pilkarza', 'id_meczu', 'gole', 'asysty', 'faule', 'zolta', 'czerwona',)
    def clean_gole(self):
        gole = self.cleaned_data['gole']
        if gole < 0:
            raise forms.ValidationError('Błędna liczba.')
        return gole
    def clean_asysty(self):
        asysty = self.cleaned_data['asysty']
        if asysty < 0:
            raise forms.ValidationError('Błędna liczba.')
        return asysty
    def clean_faule(self):
        faule = self.cleaned_data['faule']
        if faule < 0:
            raise forms.ValidationError('Błędna liczba.')
        return faule

class PilkarzForm(forms.ModelForm):
    imie = forms.TextInput()
    nazwisko = forms.TextInput()
    data_urodzenia = forms.DateInput()
    class Meta:
        model = Pilkarz
        fields = ('id_klubu', 'imie', 'nazwisko', 'data_urodzenia', 'id_pozycji',)
        widgets = {
            'imie': forms.TextInput(attrs={'style': 'width:250px', 'pattern':'[a-zA-Z]+', 'title':'Imie może zawierać tylko litery.'}),
            'nazwisko': forms.TextInput(attrs={'style': 'width:250px', 'pattern':'[a-zA-Z]+', 'title':'Nazwisko może zawierać tylko litery.'}),
            'data_urodzenia':  forms.DateInput(attrs={'type': 'date'}),
        }
    #Walidacja danych wejściowych#
    def clean_data_urodzenia(self):
        data = self.cleaned_data['data_urodzenia']
        if data > datetime.date.today() - datetime.timedelta(days=(15 * 365.24)):
            raise forms.ValidationError('Niepoprawna data! Zawodnik musi mieć co najmniej 16 lat')
        return data
    def clean_imie(self):
        imiee = self.cleaned_data['imie']
        if imiee != imiee.capitalize():
            raise forms.ValidationError('Imie musi zaczynać się od wielkiej litery.')
        return imiee
    def clean_nazwisko(self):
        nazwiskoo = self.cleaned_data['nazwisko']
        if nazwiskoo != nazwiskoo.capitalize():
            raise forms.ValidationError('Nazwisko musi zaczynać się od wielkiej litery.')
        return nazwiskoo
#Formularz logowania dla organizatorów
class LoginForm(forms.Form):
    login = forms.CharField()
    hasło = forms.CharField(widget=forms.PasswordInput)