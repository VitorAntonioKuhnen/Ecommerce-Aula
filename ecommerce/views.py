from django.shortcuts import render
from .models import Produto


def inicio(request):
    return render(request, 'inicio/index.html')

def dashboard(request):
    valorTot = 0
    qtd = 0
    for pd in Produto.objects.all():
        valorTot += pd.valor
        qtd += pd.qtd
    return render(request, 'index.html', {'valorTot':valorTot, 'qtd':qtd})


def estoque(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/index.html',{'produtos':produtos})