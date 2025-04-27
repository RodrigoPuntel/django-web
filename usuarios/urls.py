from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('srq/', views.aplicar_srq, name='aplicar_srq'),
    path('resultado/<str:resultado>/', views.resultado_view, name='resultado_srq'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
