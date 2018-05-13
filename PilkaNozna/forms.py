from django import forms

from .models import Liga

class PostForm(forms.ModelForm):

    class Meta:
        model = Liga
        fields = ('nazwa_ligi',)