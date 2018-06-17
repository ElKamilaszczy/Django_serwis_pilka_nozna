from django import forms
from .models import Liga, Klub, Pilkarz, Mecz, Statystyki_gracza, Email
from django.core.validators import RegexValidator, MinValueValidator
import datetime
class LigaForm(forms.ModelForm):
    class Meta:
        model = Liga
        fields = ('nazwa_ligi',)
        widgets = {
            'nazwa_ligi': forms.TextInput(attrs = {'style': 'width:250px', 'title': 'Podaj nazwę ligi.'}),
        }
    def clean_nazwa_ligi(self):
        nazwa = self.cleaned_data['nazwa_ligi']
        nazwy_lig = Liga.objects.all()
        for n in nazwy_lig:
            if n.nazwa_ligi == nazwa:
                raise forms.ValidationError("Nazwa jest już zajęta.")
        return nazwa

class KlubForm(forms.ModelForm):
    nazwa_klubu = forms.TextInput()
    class Meta:
        model = Klub
        fields = ('nazwa_klubu', 'id_ligi',)
        widgets = {
            'nazwa_klubu': forms.TextInput(attrs = {'style': 'width:250px', 'title': 'Podaj nazwę klubu.'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        klub = cleaned_data.get("nazwa_klubu")
        print(klub)
        print(type(klub))
        liga = cleaned_data.get("id_ligi")
        kluby = Klub.objects.filter(id_ligi = liga)
        if not klub:
            raise forms.ValidationError("Pola wymagane")
        if not liga:
            raise forms.ValidationError("Pole wymagane")
        for k in kluby:
            if klub == k.nazwa_klubu:
                raise forms.ValidationError("W tej lidze istnieje już klub o tej samej nazwie")
        if klub != klub.capitalize():
            raise forms.ValidationError('Nazwa klubu musi rozpoczynać się od wielkiej litery.')
        return cleaned_data

class MeczForm(forms.ModelForm):
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
        if data > datetime.date.today() + datetime.timedelta(days=(21)):
            raise forms.ValidationError('Nie można wprowadzić daty meczu ponad 21 dni naprzód od aktualnej daty.')
        if data < datetime.date.today() - datetime.timedelta(days=(21)):
            raise forms.ValidationError('Nie można wprowadzić daty meczu ponad 21 dni wcześniej od aktualnej daty.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        id_klubu1 = cleaned_data.get("id_klubu1")
        id_klubu2 = cleaned_data.get("id_klubu2")
        kl1 = Klub.objects.all().get(id_klubu = id_klubu1.id_klubu)
        kl2 = Klub.objects.all().get(id_klubu = id_klubu2.id_klubu)
        if kl1.id_ligi != kl2.id_ligi:
            raise forms.ValidationError('Drużyny z innych lig nie mogą rozgrywać ze sobą meczów.')
        if id_klubu1.id_klubu == id_klubu2.id_klubu:
            raise forms.ValidationError('Błąd - 2 takie same drużyny.')
        return cleaned_data

class StatystykiForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()
        pilkarz = cleaned_data.get("id_pilkarza")
        mecz = cleaned_data.get("id_meczu")
        if pilkarz.id_klubu.id_klubu != mecz.id_klubu1.id_klubu and pilkarz.id_klubu.id_klubu != mecz.id_klubu2.id_klubu:
            raise forms.ValidationError('Zawodnik nie jest graczem tych klubów!')
        return cleaned_data

class PilkarzForm(forms.ModelForm):
    imie = forms.TextInput()
    nazwisko = forms.TextInput()
    data_urodzenia = forms.DateInput()
    class Meta:
        model = Pilkarz
        fields = ('id_klubu', 'imie', 'nazwisko', 'data_urodzenia', 'id_pozycji',)
        widgets = {
            'imie': forms.TextInput(attrs={'style': 'width:250px', 'pattern':'[a-zA-Z]+', 'title':'Imie może zawierać tylko litery.', 'verbose_name':'Imię'}),
            'nazwisko': forms.TextInput(attrs={'style': 'width:250px', 'pattern':'[a-zA-Z]+', 'title':'Nazwisko może zawierać tylko litery.'}),
            'data_urodzenia': forms.DateInput(attrs={'type': 'date', 'title': 'Podaj lub wybierz datę.'}),
        }
    #Walidacja danych wejściowych#
    def clean_data_urodzenia(self):
        data = self.cleaned_data['data_urodzenia']
        if data > datetime.date.today() - datetime.timedelta(days=(15 * 365.24)):
            raise forms.ValidationError('Niepoprawna data! Zawodnik musi mieć co najmniej 16 lat')
        if data < datetime.date.today() - datetime.timedelta(days=(60 * 365.24)):
            raise forms.ValidationError('Piłkarz musi mieć mniej niz 60 lat.')
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

from django.core.validators import validate_email
from django.core.validators import ValidationError
class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('temat', 'tresc',)
        widgets = {
           'temat': forms.TextInput(attrs = {'style': 'width:250px','title':'Imie może zawierać tylko litery.'}),
            'tresc': forms.Textarea(),
        }
        def clean_temat(self):
            temat = self.cleaned_data['temat']
            print(temat)
            if temat is None:
                raise forms.ValidationError('Podaj temat')
            return temat
'''
from mapwidgets.widgets import GooglePointFieldWidget

class CityAdminForm(forms.ModelForm):
    class Meta:
        model = Miasto
        fields = ("coordinates", "city_hall")
        widgets = {
            'coordinates': GooglePointFieldWidget,
            'city_hall': GooglePointFieldWidget,
        }
'''