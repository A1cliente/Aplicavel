from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Corrida

class CadastroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefone', 'tipo', 'password1', 'password2']

class CorridaForm(forms.ModelForm):
    class Meta:
        model = Corrida
        fields = ['origem', 'destino']
