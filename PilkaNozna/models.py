'''
Kamil Jarmoc, Jan Kucharski

'''
from datetime import datetime
from django.db import models

# Create your models here.
class Email(models.Model):
    imie = models.CharField(max_length=25)
    email = models.EmailField()
    temat = models.CharField(max_length=100)
    tresc = models.CharField(max_length=500)

class Liga(models.Model):
    id_ligi = models.AutoField(primary_key = True, verbose_name="Liga")
    nazwa_ligi = models.TextField(verbose_name="Nazwa ligi")
    class Meta:
        verbose_name_plural = "Liga"

    def __str__(self):
        return self.nazwa_ligi

class Pozycja(models.Model):
    id_pozycji = models.AutoField(primary_key=True, verbose_name="Pozycja")
    nazwa_pozycji = models.TextField(verbose_name="Pozycja")
    class Meta:
        verbose_name_plural = "Pozycja"

    def __str__(self):
        return self.nazwa_pozycji

class Klub(models.Model):
    id_klubu = models.AutoField(primary_key = True, verbose_name="Klub")
    id_ligi = models.ForeignKey(Liga, on_delete = models.CASCADE, verbose_name="Liga")
    nazwa_klubu = models.TextField(verbose_name="Nazwa klubu")

    class Meta:
        verbose_name_plural = "Klub"

    def __str__(self):
        return self.nazwa_klubu

class Pilkarz(models.Model):
    id_pilkarza = models.AutoField(primary_key = True, verbose_name="Piłkarz")
    imie = models.TextField(verbose_name="Imię")
    nazwisko = models.TextField(verbose_name="Nazwisko")
    data_urodzenia = models.DateField()
    id_klubu = models.ForeignKey(Klub, on_delete = models.CASCADE, verbose_name="Klub")
    id_pozycji = models.ForeignKey(Pozycja, on_delete = models.CASCADE, verbose_name="Pozycja")

    class Meta:
        verbose_name_plural = "Piłkarz"

    def __str__(self):
        return "{} {}".format(self.imie,self.nazwisko)

    def klub(self):
        return self.id_klubu

    def wiek_pilkarza(self):
        return datetime.now().year - self.data_urodzenia.year

class Mecz(models.Model):
    id_meczu = models.AutoField(primary_key = True, verbose_name="Mecz")
    id_klubu1 = models.ForeignKey(Klub, on_delete = models.CASCADE, related_name="Klub_1", verbose_name="Klub 1")
    id_klubu2 = models.ForeignKey(Klub, on_delete = models.CASCADE, related_name="Klub_2", verbose_name="Klub 2")
    kolejka = models.IntegerField()
    data_meczu = models.DateField()

    class Meta:
        verbose_name_plural = "Mecz"

    def __str__(self):
        return "{}  - {}, kolejka: {}".format(self.id_klubu1, self.id_klubu2, self.kolejka)

class Statystyki_gracza(models.Model):
    zolta_choices = (
        (0, '0'),
        (1, '1'),
        (2, '2'),

    )
    czerwona_choices = (
        (0, '0'),
        (1, '1'),
    )
    id_statystyki = models.AutoField(primary_key = True)
    id_pilkarza = models.ForeignKey(Pilkarz, on_delete = models.CASCADE, verbose_name="Piłkarz")
    id_meczu = models.ForeignKey(Mecz, on_delete = models.CASCADE, verbose_name="Mecz")
    gole = models.IntegerField()
    asysty = models.IntegerField()
    faule = models.IntegerField()
    zolta = models.IntegerField(choices=zolta_choices, default = 0, verbose_name="Żółte kartki")
    czerwona = models.IntegerField(choices= czerwona_choices, default = 0, verbose_name="Czerwone kartki")

    class Meta:
        verbose_name_plural = "Statystyki"

    def __str__(self):
        return "{}, - kolejka: {}".format(self.id_pilkarza,self.id_meczu.kolejka)

'''
from mapwidgets.widgets import GooglePointFieldWidget

class Miasto(models.Model):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
'''