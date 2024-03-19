from django import forms
from .models import DatosGeneralesEmpleado,DatosOficialesEmpleado,Curso

class DatosGeneralesForm(forms.ModelForm):
    
    class Meta:
        model = DatosGeneralesEmpleado
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ap_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'ap_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control'}),
            'cuip': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email_particular': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ciudad_particular': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_particular': forms.TextInput(attrs={'class': 'form-control'}),
            'colonia_particular': forms.TextInput(attrs={'class': 'form-control'}),
            'escolaridad': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'cursos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'activo'  : forms.CheckboxInput(attrs= {'class': 'form-check-input'}),
            'numero_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        
        
class DatosOficialesForm(forms.ModelForm):
    
    class Meta:
        model = DatosOficialesEmpleado
        fields = '__all__'
        widgets = {
            'fecha_ingreso' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sueldo_base' : forms.TextInput(attrs={'class': 'form-control'}),
            'compensacion' : forms.TextInput(attrs={'class': 'form-control'}),
            'puesto' : forms.Select(attrs={'class':'form-control'}),
            'plaza' : forms.Select(attrs={'class':'form-control'}),
            'email_oficial' :  forms.EmailInput(attrs={'class':'form-control'}),
            'area' : forms.Select(attrs={'class':'form-control'}),
            'direccion' : forms.Select(attrs={'class':'form-control'}),
            'departamento' : forms.Select(attrs={'class':'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'datos_generales': forms.Select(attrs={'class': 'form-control'}),
            'zona' : forms.Select(attrs={'class': 'form-control'}),
            'examen_c3': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'posicion' : forms.TextInput(attrs={'class': 'form-control'}),
            }
     