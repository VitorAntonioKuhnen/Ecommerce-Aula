from django.shortcuts import render
from .models import Produto, Prod_Destaque


def inicio(request):
    # produtos = Produto.objects.all()
    # count = 0
    # produto = [] 
    # for pd in :
    # produto = Produto.objects.raw('select * from produto limit 4')
    # print(Produto.objects.raw('select * from ecommerce_produto limit 4'))
    return render(request, 'inicio/index.html', {'produto':Produto.objects.raw('select * from ecommerce_produto limit 4'), 'destaq':Prod_Destaque.objects.all()})

def dashboard(request):
    valorTot = 0
    qtd = 0
    for pd in Produto.objects.all():
        valorTot += pd.qtd * pd.valor
        qtd += pd.qtd
    return render(request, 'index.html', {'valorTot':valorTot, 'qtd':qtd})


def estoque(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/index.html',{'produtos':produtos})