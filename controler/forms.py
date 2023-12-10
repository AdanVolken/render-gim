from .models import Cliente,Pago,Dia
from django import forms

class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields= '__all__'



class FormularioPago(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['mes', 'monto']
        
class FormularioDia(forms.ModelForm):
    class Meta:
        model = Dia
        fields = ['dia','numero', 'hora']