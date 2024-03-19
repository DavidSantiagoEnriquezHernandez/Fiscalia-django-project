from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('base/', views.base, name='base'),
    path('signout/', views.signout, name = 'signout'),
    path('registeruser/', views.register_user, name = 'registeruser'),
    path('showuser/', views.show_user, name = 'showuser'),
    path('registeruser/<int:empleado_id>/', views.register_user, name='edituser'),
    path('exportar_empleados/', views.export_to_excel, name='export_users'),
]
