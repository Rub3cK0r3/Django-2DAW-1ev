from django import forms

class FormularioFiltroEditores(forms.Form):
    pais = forms.CharField(
        label="buscar_por_PAIS",
        max_length=50,
        required=False, # es un filtro opcional
        widget=forms.TextInput()
    )