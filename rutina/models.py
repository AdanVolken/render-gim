from django.db import models

# Create your models here.

class Ejercicio(models.Model):
    nombre = models.CharField(max_length= 50)
    imagen = models.ImageField(upload_to= "rutina/image/")
    
    def __str__(self):
        return self.nombre
    
class Rutina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ejercicios = models.ManyToManyField(Ejercicio)
    
    def __str__(self):
        return self.nombre
    

