from django.shortcuts import render, get_object_or_404, redirect
from .models import Rutina, Ejercicio
from .forms import FormularioEjercicio,FormularioRutinas
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def rutina(request):
    rutinas = Rutina.objects.all()
    rutina_add = FormularioRutinas()

    if request.method == "POST":
        rutina_add = FormularioRutinas(request.POST, request.FILES)
        if rutina_add.is_valid():
            nombre = rutina_add.cleaned_data['nombre']
            descripcion = rutina_add.cleaned_data['descripcion']
            ejercicios = rutina_add.cleaned_data['ejercicios']
                
            nueva_rutina = Rutina(nombre=nombre, descripcion=descripcion)
            nueva_rutina.save()

            # Agregamos los ejercicios a la rutina utilizando el método set
            nueva_rutina.ejercicios.set(ejercicios)

            # Puedes agregar un mensaje de éxito si lo deseas
            return render(request, 'rutinas.html', {'form_rutina': rutina_add, 'rutinas': rutinas, 'mensaje': 'Rutina agregada exitosamente'})

    return render(request, 'rutinas.html', {'rutinas': rutinas, 'form_rutina': rutina_add})

@login_required   
def rutina_detail(request, id):
    rutina = get_object_or_404(Rutina, pk = id)
    ejercicios = Ejercicio.objects.filter(rutina=id)
    return render(request, 'rutina_id.html', {
        'rutina' : rutina,
        'ejercicios': ejercicios
    })


@login_required    
def ejercicios(request):
    ejercicio = Ejercicio.objects.all()
    return render(request,'ejercicio.html', {
        'ejercicios': ejercicio
    })


@login_required    
def agregar_ejercicio(request):
    if request.method == "POST":
        ejercicio = FormularioEjercicio(request.POST, request.FILES)
        if ejercicio.is_valid():
            nombre = ejercicio.cleaned_data['nombre']
            imagen = ejercicio.cleaned_data['imagen']
            
            nuevo_ejercicio = Ejercicio(nombre=nombre, imagen=imagen)
            nuevo_ejercicio.save()

            # Puedes agregar un mensaje de éxito si lo deseas
            return render(request, 'agregar_ejercicio.html', {'form': ejercicio, 'mensaje': 'Ejercicio agregado exitosamente'})

    else:
        ejercicio = FormularioEjercicio()

    return render(request, 'agregar_ejercicio.html', {'form': ejercicio})


##################################################################################################################
#Editar Registros de Formularios
##################################################################################################################

# Edit Ejercicios
@login_required
def editar_ejercicio(request, id_ejercicio):
    ejercicio = get_object_or_404(Ejercicio, pk = id_ejercicio)
    form = FormularioEjercicio(instance=ejercicio)
    return render(request, 'editar_ejercicio.html',{
        'form': form, 'ejercicio': ejercicio
    })
    
@login_required    
def actualizar_ejercicio(request, id_ejercicio):
    ejercicio = Ejercicio.objects.get(id = id_ejercicio)
    form_actualizado = FormularioEjercicio(request.POST ,instance=ejercicio)
    if form_actualizado.is_valid():
        form_actualizado.save()
        
    ejercicio = Ejercicio.objects.all()
    return render(request,'ejercicio.html', {
        'ejercicios': ejercicio
    })
 
@login_required   
# Edir Rutina
def editar_rutina(request, id_rutina):
    rutina = get_object_or_404(Rutina, pk = id_rutina)
    form_rutina = FormularioRutinas(instance= rutina)
    return render(request,'editar_rutina.html', {
        'rutina': rutina, 'form': form_rutina
    })
  
@login_required  
def actualizar_rutina(request, id_rutina):
    rutina = Rutina.objects.get(id = id_rutina)
    rutina_actualizado = FormularioRutinas(request.POST, instance=rutina)
    if rutina_actualizado.is_valid():
        rutina_actualizado.save()
        return redirect('rutina_id', id=id_rutina)
        
    form_rutina = FormularioRutinas(instance=rutina)
    return render(request, 'editar_rutina.html', {
        'rutina': rutina,
        'form': form_rutina
    })