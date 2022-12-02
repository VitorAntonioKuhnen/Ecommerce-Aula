from django.shortcuts import render,redirect
from .models import Produto, Prod_Destaque, Carrinho, Categoria, Hist_Produto
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
    categoria = Categoria.objects.raw('select * from ecommerce_categoria limit 3')
    parcela = '{:.2f}'.format(produto.valor/12)
    return render(request, 'clientes/produto/index.html', {'produto':produto, 'parcela':parcela, 'categoria':categoria})    

def categorias(request):
    categoria = Categoria.objects.raw('select * from ecommerce_categoria limit 3')
    produtos = Produto.objects.all()
    return render(request, 'clientes/categorias/index.html', {'produtos':produtos, 'categoria':categoria})   

def buscar(request):
    categoria = Categoria.objects.raw('select * from ecommerce_categoria limit 3')
    busca = request.GET.get('pesquisa')
    produtos = Produto.objects.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca))
    return render(request, 'clientes/categorias/index.html', {'produtos':produtos, 'categoria':categoria})          


def adicionaCart(request, id):
    user = request.user.id
    cart = Carrinho.objects.filter(usuario_id=user, status = 'A') 
    pega_Produto = Produto.objects.get(id=id)

    if cart:
       
        hist_prod = Hist_Produto.objects.filter(Q(usuario_id = user) & Q(produto_id = pega_Produto.id) & Q(carrinho='A'))
        # hist_prod = Hist_Produto.objects.filter(usuario_id = user, produto_id = pega_Produto.id, carrinho='A')

        for pr in hist_prod:
            pr.qtd +=1
            pr.save()
            print(pr.qtd)
            
        hist_prod.qtd +=1
        hist_prod.save()
        cart = Carrinho.objects.get(usuario_id = user)
        cart.produto.add(pega_Produto)
    else:   
        Hist_Produto.objects.create(produto_id = pega_Produto.id, valor_uni=pega_Produto.valor, qtd=1, usuario_id=user, movimentacao='E', carrinho='A')
        add_Carrinho = Carrinho.objects.create(usuario_id=user, status='A')
        add_Carrinho.produto.add(pega_Produto)

    return redirect(produto, id)