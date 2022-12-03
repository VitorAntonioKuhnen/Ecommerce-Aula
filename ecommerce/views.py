from django.shortcuts import render,redirect
from .models import Produto, Prod_Destaque, Carrinho, Categoria, Hist_Produto
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum 

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
    carrinhos = Carrinho.objects.filter(Q(usuario = request.user.id) & Q(status = 'A'))
    valor = 0
    for carrinho in carrinhos:
        # print(carrinho.id) #Correto
        print()
        for prod in carrinho.produto.all(): #Preciso percorrer minha lista de produtos para somar a quantidade
            print(prod.id)
            hist_prod = None
            hist_prod = Hist_Produto.objects.get(usuario_id = request.user.id, produto_id = prod.id, carrinho = 'A')
            print('Quantidade')
            print(hist_prod.valor_uni * hist_prod.qtd)

            valor += hist_prod.valor_uni * hist_prod.qtd #Precisa ser ajustado
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
        print(pega_Produto.id)
        cart = Carrinho.objects.get(usuario_id = user)
        cart.produto.add(pega_Produto)
        hist_prod = Hist_Produto.objects.get(Q(usuario_id = user) & Q(produto_id = pega_Produto.id) & Q(carrinho='A'))
        print(hist_prod)
        if Hist_Produto.objects.filter(Q(usuario_id = user) & Q(produto_id = pega_Produto.id) & Q(carrinho='A')) is False:
            Hist_Produto.objects.create(produto_id = pega_Produto.id, valor_uni=pega_Produto.valor, qtd=1, usuario_id=user, movimentacao='E', carrinho='A')
        else:
            print('não entrou')
        # hist_prod = Hist_Produto.objects.get(Q(usuario_id = user) & Q(produto_id = pega_Produto.id) & Q(carrinho='A'))
        # hist_prod.qtd +=1
        # hist_prod.save() 
        
    else:   
        Hist_Produto.objects.create(produto_id = pega_Produto.id, valor_uni=pega_Produto.valor, qtd=1, usuario_id=user, movimentacao='E', carrinho='A')
        add_Carrinho = Carrinho.objects.create(usuario_id=user, status='A')
        add_Carrinho.produto.add(pega_Produto)

    return redirect(produto, id)