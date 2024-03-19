from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from .forms import DatosGeneralesForm, DatosOficialesForm
from .models import DatosGeneralesEmpleado, DatosOficialesEmpleado
from django.contrib.auth import get_user_model
import xlsxwriter
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
# Create your views here.
CustomUser = get_user_model()
def signin(request):
    if request.method == "GET":
        return render(request, 'core/signin.html', {'form': AuthenticationForm})

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:base')
        else:
            return render(request, 'core/signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        


@login_required
def base(request):
    username = request.user.username
    return render(request, 'core/base.html', {
        'username': username
    })


def signout(request):
    logout(request)
    return redirect('core:signin')

@login_required
def register_user(request, empleado_id=None):
    
    if empleado_id:
        empleado = get_object_or_404(DatosGeneralesEmpleado, pk=empleado_id)
    else:
        empleado = None

    datos_oficiales = None

    if empleado and empleado.usuario:
        datos_oficiales = DatosOficialesEmpleado.objects.filter(usuario=empleado.usuario).first()

    if request.method == 'POST':
        datos_generales_form = DatosGeneralesForm(request.POST, request.FILES, instance=empleado, prefix='datos_generales')
        datos_oficiales_form = DatosOficialesForm(request.POST, instance=datos_oficiales, prefix='datos_oficiales')

        if datos_generales_form.is_valid() and datos_oficiales_form.is_valid():
            datos_generales = datos_generales_form.save()
            datos_oficiales = datos_oficiales_form.save(commit=False)
            datos_oficiales.usuario = datos_generales.usuario
            datos_oficiales.save()
            messages.success(request, '¡Empleado registrado exitosamente!')
            return redirect('core:registeruser')
    else:
        datos_generales_form = DatosGeneralesForm(instance=empleado, prefix='datos_generales')
        datos_oficiales_form = DatosOficialesForm(instance=datos_oficiales, prefix='datos_oficiales')

    return render(request, 'core/registeruser.html', {
        'datos_generales_form': datos_generales_form,
        'datos_oficiales_form': datos_oficiales_form,
    })
@login_required
def show_user(request):
    datos_empleados_generales = DatosGeneralesEmpleado.objects.all()
    query = request.GET.get('q')
    
  
    if query:
        datos_empleados_generales = datos_empleados_generales.filter(
            nombre__icontains=query) | \
            datos_empleados_generales.filter(ap_paterno__icontains=query) | \
            datos_empleados_generales.filter(ap_materno__icontains=query) | \
            datos_empleados_generales.filter(activo=query.lower() == 'activo')
    
    return render(request, 'showuser.html', {'datos_generales': datos_empleados_generales})



def export_to_excel(request):
    datos_empleados = DatosGeneralesEmpleado.objects.all()

    libro_excel = xlsxwriter.Workbook('empleados.xlsx')
    hoja_excel = libro_excel.add_worksheet('Empleados')

    formato_encabezado = libro_excel.add_format({'bold': True})
    formato_fecha = libro_excel.add_format({'num_format': 'dd-mm-yyyy'})
    formato_fechita = libro_excel.add_format({'num_format': 'dd-mm-yyyy'})
    # Encabezados de columnas para los datos generales
    columnas_generales = ['Nombre', 'Apellido Paterno', 'Apellido Materno', 'Estado']
    for col, columna in enumerate(columnas_generales):
        hoja_excel.write(0, col, columna, formato_encabezado)

    # Encabezados de columnas para los datos oficiales
    columnas_oficiales = ['Puesto', 'Sueldo base','Fecha de ingreso','Compensación','Plaza','Email oficial','Área','Dirección','Departamento','Zona','Fecha examén C3','Posición','Fecha de nacimiento','CURP','CUIP','Teléfono celular','Email particular','Ciudad particular','Dirección','Colonia particular','Escolaridad','Género','Estado civil','Cursos','Número de empleado']  # Ajusta según tus campos de DatosOficialesEmpleado
    for col, columna in enumerate(columnas_oficiales, start=len(columnas_generales)):
        hoja_excel.write(0, col, columna, formato_encabezado)

    # Escribir datos de empleados
    for fila, empleado in enumerate(datos_empleados, start=1):
        # Escribir datos generales
        hoja_excel.write(fila, 0, empleado.nombre)
        hoja_excel.write(fila, 1, empleado.ap_paterno)
        hoja_excel.write(fila, 2, empleado.ap_materno)
        hoja_excel.write(fila, 3, 'Activo' if empleado.activo else 'Inactivo')
        
        cursos_empleado = ', '.join(curso.nombre for curso in empleado.cursos.all())
        hoja_excel.write(fila, 27, cursos_empleado)

        # Obtener datos oficiales del empleado
        datos_oficiales = DatosOficialesEmpleado.objects.filter(usuario=empleado.usuario).first()
        if datos_oficiales:
            
            if isinstance(datos_oficiales.fecha_ingreso, str):
                fecha_ingreso = datetime.strptime(datos_oficiales.fecha_ingreso, '%d-%m-%Y')  # Ajusta el formato según tus datos
            else:
                fecha_ingreso = datos_oficiales.fecha_ingreso

            if isinstance(datos_oficiales.examen_c3, str):
                fecha_examen = datetime.strptime(datos_oficiales.examen_c3, '%d-%m-%Y')
            else:
                fecha_examen = datos_oficiales.examen_c3
                
            if isinstance(empleado.fecha_nacimiento, str):
                fecha_nac = datetime.strptime(empleado.fecha_nacimiento, '%d-%m-%Y')
            else:
                fecha_nac = empleado.fecha_nacimiento
            
            
            hoja_excel.write(fila, 4, datos_oficiales.puesto)
            hoja_excel.write(fila, 5, datos_oficiales.sueldo_base)
            hoja_excel.write_datetime(fila, 6, fecha_ingreso, formato_fecha)
            hoja_excel.write(fila, 7, datos_oficiales.compensacion)
            hoja_excel.write(fila, 8, datos_oficiales.plaza)
            hoja_excel.write(fila, 9, datos_oficiales.email_oficial)
            hoja_excel.write(fila, 10, datos_oficiales.area.nombre)
            hoja_excel.write(fila, 11, datos_oficiales.direccion.nombre)
            hoja_excel.write(fila, 12, datos_oficiales.departamento.nombre)
            hoja_excel.write(fila, 13, datos_oficiales.zona.nombre)
            hoja_excel.write_datetime(fila, 14, fecha_examen, formato_fechita)
            hoja_excel.write(fila, 15, datos_oficiales.posicion)
            hoja_excel.write(fila, 16, fecha_nac, formato_fecha)
            hoja_excel.write(fila, 17, empleado.curp)
            hoja_excel.write(fila, 18, empleado.cuip)
            hoja_excel.write(fila, 19, empleado.tel_celular)
            hoja_excel.write(fila, 20, empleado.email_particular)
            hoja_excel.write(fila, 21, empleado.ciudad_particular)
            hoja_excel.write(fila, 22, empleado.direccion_particular)
            hoja_excel.write(fila, 23, empleado.colonia_particular)
            hoja_excel.write(fila, 24, empleado.escolaridad)
            hoja_excel.write(fila, 25, empleado.genero)
            hoja_excel.write(fila, 26, empleado.estado_civil)
            hoja_excel.write(fila, 28, empleado.numero_empleado)
            
            
            
            
            

    libro_excel.close() 

    with open('empleados.xlsx', 'rb') as archivo_excel:
        archivo_excel_data = archivo_excel.read()

    response = HttpResponse(archivo_excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=empleados.xlsx'
    return response
