import datetime
from datetime import timezone
from django.db import models
from django.utils.timezone import datetime
from rutina.models import Rutina

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField(unique=True)
    rutina = models.ForeignKey(Rutina,blank=True, null=True, on_delete=models.SET_NULL)
    

    def __str__(self):
        return self.nombre
    

class Dia(models.Model):
    dia = models.CharField(max_length=15)
    numero = models.IntegerField()
    hora = models.TimeField(default=datetime.now().time()) 
    clientes = models.ForeignKey(Cliente, blank=True, on_delete=models.CASCADE)
    



class Pago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True) 
    mes = models.CharField(max_length=25)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null= True)

    def __str__(self):
        return self.fecha_creacion
    
