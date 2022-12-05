from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('dashboard/estoque/', views.estoque, name='estoque'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('categorias/', views.categorias, name='categorias'),
    path('produto/<int:id>/', views.produto, name='produto'),
    path('buscar/', views.buscar, name='buscar'),
    path('adicionaCart/<int:id>/', views.adicionaCart, name='adicionaCart'),
    path('perfil/', views.perfil, name='perfil'),
    path('dashboard/sacs/', views.sacs, name='sacs'),
    path('comprar/<int:id>/', views.comprar, name='comprar'),
    path('finalizar/', views.finalizar, name='finalizar'),
]