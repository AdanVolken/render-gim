from django import forms
from .models import Ejercicio, Rutina

class FormularioRutinas(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = '__all__'
        
class FormularioEjercicio(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre','imagen']