from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DatosGeneralesEmpleado,DatosOficialesEmpleado,Zona,Area,Direccion,Departamento,Curso
admin.site.register(CustomUser, UserAdmin)
admin.site.register(DatosGeneralesEmpleado)
admin.site.register(DatosOficialesEmpleado)
admin.site.register(Zona)
admin.site.register(Area)
admin.site.register(Departamento)
admin.site.register(Direccion)
admin.site.register(Curso)
# Register your models here.