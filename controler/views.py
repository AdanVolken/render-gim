
from django.http import HttpResponse
from django.shortcuts import redirect, render , get_object_or_404
from django.contrib.auth import login,authenticate 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import FormularioCliente,FormularioPago,FormularioDia
from .models import Cliente,Pago,Dia
from django.db.models import Sum
from datetime import date as d
from django.contrib.auth.decorators import login_required

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape

from PIL import Image

# Create your views here.

def home(request):
    return render(request, 'index.html')



def sesion(request):
    if request.method == 'POST':
            user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('cliente')
            else:
                return redirect('sesion', {
                    "error": "Usuario o Contraseña Incorrecta"})  # Redirigir de nuevo a la página de inicio de sesión
    else:  # Método GET
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    
def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except :
                return render(request, 'registro.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'registro.html', {"form": UserCreationForm, "error": "Passwords did not match."})
    
@login_required
def cliente(request):
    clientes = Cliente.objects.all().order_by('nombre')
    # Calcular el monto total de los pagos para cada cliente
    # Obtener la fecha actual
    fecha_actual = d.today()

    # Calcular la suma de todos los pagos para la fecha actual
    suma_pagos = Pago.objects.filter(
        fecha_creacion__date=fecha_actual
    ).aggregate(Sum('monto'))['monto__sum'] or 0.0
    
    #Formulario para agregar  Cliente
    formulario_cliente = FormularioCliente()
    if request.method == 'POST':
        formulario_cliente = FormularioCliente(request.POST)
        if formulario_cliente.is_valid():
            nombre = formulario_cliente.cleaned_data['nombre']
            apellido = formulario_cliente.cleaned_data['apellido']
            dni = formulario_cliente.cleaned_data['dni']
            rutina = formulario_cliente.cleaned_data['rutina']
            cliente = Cliente(nombre =nombre, apellido = apellido, dni= dni, rutina= rutina)
            cliente.save()
    
    formulario_cliente = FormularioCliente()
    return render(request, 'clientes.html', {
        'clientes': clientes,
        'suma_pagos': suma_pagos,
        'fecha_actual': fecha_actual,
        'form' : formulario_cliente,
    })

@login_required
def cliente_detail(request, id):
    cliente = get_object_or_404(Cliente, pk=id) 
    cliente.monto_total_pagos = cliente.pago_set.aggregate(Sum('monto'))['monto__sum'] or 0.0
    form = FormularioPago()
    pagos = Pago.objects.filter(cliente=id).order_by("-fecha_creacion")[:5]
    form_dia = FormularioDia()
    dias = Dia.objects.filter(clientes=id).order_by('numero')
    
    # Recuperar los ejercicios de la rutina del cliente
    rutina_ejercicios = []
    if cliente.rutina:
        rutina_ejercicios = cliente.rutina.ejercicios.all()

    if request.method == 'GET':
        return render(request, 'cliente_id.html', {
            'cliente': cliente,
            'form': form,
            'form_dia': form_dia,
            'dias': dias,
            'pagos': pagos,
            'rutina_ejercicios': rutina_ejercicios,
        })

    else:
        form = FormularioPago(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            mes = form.cleaned_data['mes']
            monto = form.cleaned_data['monto']
            # Crear una instancia del modelo Pago asociada al cliente actual
            pago = Pago(cliente=cliente, mes=mes, monto=monto)
            # Guardar la instancia del modelo en la base de datos
            pago.save()
    # Formulario de dia de dia de rutina
    if request.method == 'POST':
            form_dia = FormularioDia(request.POST)
            if form_dia.is_valid():
                # Obtener los datos del formulario
                dia = form_dia.cleaned_data['dia']
                numero = form_dia.cleaned_data['numero']
                hora = form_dia.cleaned_data['hora']
                # Agregamos los datos del clinte que estamos usando
                dia_rutina = Dia(clientes=cliente, dia=dia, numero=numero, hora=hora)
                #Guardamos los datos en la BDD
                dia_rutina.save()
            else :    
                form_dia = FormularioDia()            
                form = FormularioPago()    
                return render(request, 'cliente_id.html',{
                    'cliente':cliente,
                    'form':form,
                    'form_dia':form_dia,
                    'pagos': pagos,
                    'rutina_ejercicios': rutina_ejercicios,
                    'error_dia': 'Dato Guardado'
                    })
                   
    cliente = get_object_or_404(Cliente, pk=id) 
    cliente.monto_total_pagos = cliente.pago_set.aggregate(Sum('monto'))['monto__sum'] or 0.0
    form = FormularioPago()
    pagos = Pago.objects.filter(cliente=id)
    form_dia = FormularioDia()
    dias = Dia.objects.filter(clientes=id).order_by('numero')
    return render(request, 'cliente_id.html', {
            'cliente': cliente,
            'form': form,
            'form_dia': form_dia,
            'dias': dias,
            'pagos': pagos,
            'rutina_ejercicios': rutina_ejercicios,
        })

@login_required
def descargar_pdf(request, id):
    cliente = get_object_or_404(Cliente, pk=id)

    # Creamos la respuesta HTTP con el encabezado correcto para descargar el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rutina_{cliente.nombre}.pdf"'

    # Creamos el objeto PDF con ReportLab y configuramos la orientación a horizontal
    p = canvas.Canvas(response, pagesize=landscape(letter))

    # Ahora, agregamos el contenido del PDF, adaptado a tu necesidad
    p.drawString(100, 590, f'Rutina de {cliente.nombre} {cliente.apellido}')
    p.drawString(100, 570, 'Ejercicios:')

    # Obtén el tamaño real de la página
    width, height = landscape(letter)

    # Configura las dimensiones de las imágenes y la disposición en filas
    img_width = 100
    img_height = 100
    margin = 30
    exercises_per_row = 5  

    y_position = 560
    x_position = 50

    for idx, ejercicio in enumerate(cliente.rutina.ejercicios.all(), start=1):
        rect_width = img_width + 15
        rect_height = img_height + 65

        img_x_position = x_position + (rect_width - img_width) / 2
        img_y_position = y_position - rect_height + 60  

        # Dibuja un rectángulo negro alrededor de cada tarjeta de ejercicio
        p.setStrokeColorRGB(0, 0, 0)  # Color del borde negro
        p.rect(x_position, y_position - rect_height, rect_width, rect_height, stroke=1, fill=0)

        p.drawImage(ejercicio.imagen.path, img_x_position, img_y_position, width=img_width, height=img_height)

        text_x_position = x_position + (rect_width - img_width) / 2
        text_y_position = y_position - rect_height + 30  
        p.drawString(text_x_position, text_y_position, f'{ejercicio.nombre}')

        # Ajusta la posición para el siguiente ejercicio
        x_position += img_width + margin

        # Si hemos alcanzado el número deseado de ejercicios por fila, avanza a la siguiente fila
        if idx % exercises_per_row == 0:
            y_position -= rect_height + margin
            x_position = 50  

        # Si no cabe en la página actual, añade una nueva página
        if y_position < 50:
            p.showPage()
            y_position = 750

    p.showPage()
    p.save()

    return response

@login_required        
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente,pk=id)
    actualizar_cliente = FormularioCliente(instance=cliente)
    return render(request, 'editar_cliente.html', {
        'cliente': cliente,
        'actualizar_cliente': actualizar_cliente,
    })
   

@login_required
def actualizar_cliente(request,id):
    cliente = Cliente.objects.get(pk=id)
    actualizar_cliente = FormularioCliente(request.POST, instance=cliente)
    if request.method == "POST":
        actualizar_cliente.save()
        return redirect('cliente_detail', id=id)
            


@login_required
def pagos(request):
    # Obtener la lista de días y la suma de pagos para cada día
    dias_con_pagos = Pago.objects.values('fecha_creacion__date').annotate(total_pagos=Sum('monto'))

    return render(request, 'pagos.html', {
        'dias_con_pagos': dias_con_pagos,
    })