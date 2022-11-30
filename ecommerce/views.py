from django.shortcuts import render
from .models import Produto, Prod_Destaque, Carrinho
from django.contrib.auth.decorators import login_required


def inicio(request):
    return render(request, 'clientes/inicio/index.html', {'produto':Produto.objects.raw('select * from ecommerce_produto limit 4'), 'destaq':Prod_Destaque.objects.all()})


@login_required(login_url='login') #Direiciona login para url passada
def dashboard(request):
    valorTot = 0
    qtd = 0
    for pd in Produto.objects.all():
        valorTot += pd.qtd * pd.valor
        qtd += pd.qtd
    return render(request, 'admins/dashboard/index.html', {'valorTot':valorTot, 'qtd':qtd})

def estoque(request):
    produtos = Produto.objects.all()
    return render(request, 'admins/estoque/index.html',{'produtos':produtos})

def carrinho(request):
    carrinhos = Carrinho.objects.filter(usuario = request.user.id)
    valor = 0
    for carrinho in carrinhos:
        valor += carrinho.produto.preco * carrinho.qtd_Prod
    return render(request, 'clientes/carrinho/index.html',{'carrinhos':carrinhos, 'valor':valor})    

def produto(request, id):
    produto = Produto.objects.get(id=id)
    parcela = '{:.2f}'.format(produto.valor/12)
    return render(request, 'clientes/produto/index.html', {'produto':produto, 'parcela':parcela})    

def categorias(request):
    produtos = Produto.objects.all()
    return render(request, 'clientes/categorias/index.html', {'produtos':produtos})   