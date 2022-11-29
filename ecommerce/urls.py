from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('estoque', views.estoque, name='estoque'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('carrinho', views.carrinho, name='carrinho'),
]