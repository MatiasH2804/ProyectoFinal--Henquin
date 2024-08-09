from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('register/', views.register, name='register'),
    path('registrar_ingreso/', views.registrar_ingreso, name='registrar_ingreso'),
    path('registrar_gasto/', views.registrar_gasto, name='registrar_gasto'),
    path('resumen/', views.resumen_financiero, name='resumen_financiero'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('about/', views.about, name='about'),
    path('download/', views.download_data, name='download_data'),
    path('reset/', views.reset_data, name='reset_data'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
