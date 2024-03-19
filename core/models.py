from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import genero,ecivil,puestos, plaza

# Create your models here.


class CustomUser(AbstractUser):
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='custom_user_group')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', related_query_name='custom_user_permission')

class Curso(models.Model):
    nombre  = models.CharField(max_length=70)
    academia = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
        
    def __str__(self):
        return f'{self.nombre}'
    
class Zona(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.nombre}'
    
class Area(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.nombre}'
    
class Direccion(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return f'{self.nombre}'
class Departamento(models.Model):
    nombre = models.CharField(max_length=50)
    direcciones = models.ManyToManyField(Direccion)
    
    def __str__(self):
        return f'{self.nombre}'

    
    
class DatosGeneralesEmpleado(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    ap_paterno = models.CharField(max_length=20)
    ap_materno = models.CharField(max_length=20)
    curp = models.CharField(max_length=25)
    cuip = models.CharField(max_length=25, null=True, blank=True)
    tel_celular = models.CharField(max_length=25)
    email_particular = models.EmailField(max_length=40)
    fecha_nacimiento = models.DateField()
    ciudad_particular = models.CharField(max_length=20)
    direccion_particular = models.CharField(max_length=25)
    colonia_particular = models.CharField(max_length=20)
    escolaridad = models.CharField(max_length=20)
    genero = models.CharField(max_length=20, choices=genero, default='M')
    estado_civil = models.CharField(max_length=20, choices=ecivil,  default="M")
    foto = models.ImageField(null=True, blank=True, upload_to='photos/')
    cursos = models.ManyToManyField(Curso, blank=True)
    activo = models.BooleanField(default=True)
    numero_empleado = models.CharField(max_length=20, unique=True, blank=True,null=True)

    def __str__(self):
        return f"{self.nombre} {self.ap_paterno} {self.ap_materno}"   

class DatosOficialesEmpleado(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha_ingreso =  models.DateField()
    sueldo_base = models.CharField(max_length=20)
    compensacion = models.CharField(max_length=20)
    puesto = models.CharField(max_length=100, choices=puestos, default='ANALISTA TÁCTICO')
    plaza = models.CharField(max_length=100, choices=plaza, default='BASE')
    email_oficial = models.EmailField(max_length=40,null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, default=28)
    posicion = models.CharField(max_length=30,blank=True,null=True, unique=True)
    examen_c3 = models.DateField(null=True, blank=True) 
    
    def __str__(self):
        return f"{self.usuario}"