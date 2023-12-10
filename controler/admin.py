from django.contrib import admin

from .models import Dia,Pago,Cliente

# Register your models here.
admin.site.register(Dia)
admin.site.register(Pago)
admin.site.register(Cliente)
