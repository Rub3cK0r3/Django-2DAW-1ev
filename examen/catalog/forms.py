from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import *

# USANDO FORM
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

"""
FORMULARIOS DEL EXAMEN 1ºev:
"""

class BookinstanceForm(forms.Form):
    titulo = forms.CharField(
        label="Nombre",
        max_length=50,
        required=False, # ninguno es true porque puedo querer no editarlo todo
        widget=forms.TextInput()
    )

    autor = forms.ModelChoiceField(
        label='Author',
        queryset=Author.objects.all(),
        required=False,
    )

    summary = forms.CharField(
        label="Summary",
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Un texto largo de referencia'})
    )


class GenreBookinstanceDetailForm(forms.Form):
    genero_seleccion = forms.ModelChoiceField(
        label='Seleccionar género existente',
        queryset=Genre.objects.all(),
        required=False
    )
    genero_creacion = forms.CharField(
        label="O crear un nuevo género",
        max_length=50,
        required=False,
    )



# formulario para anyadir opcionalmente el genero a un bookinstance
class GenreCheckForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['genre']
        widgets = {
            'genre': forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].required = False


class GenreAddForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name': _('Añadir un nuevo genero (opcional)'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        