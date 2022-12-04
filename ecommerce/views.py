from django.shortcuts import render, redirect
from .models import Produto, Prod_Destaque, Carrinho, Categoria, Hist_Produto, Sac
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def inicio(request):
    return render(request, 'clientes/inicio/index.html', {'produto': Produto.objects.raw('select * from ecommerce_produto limit 4'), 'destaq': Prod_Destaque.objects.all()})


@login_required(login_url='login')  # Direiciona login para url passada
def dashboard(request):
    if request.user.is_superuser:
        valorTot = 0
        qtd = 0
        for pd in Produto.objects.all():
            valorTot += pd.qtd * pd.valor
            qtd += pd.qtd
        return render(request, 'admins/dashboard/index.html', {'valorTot': valorTot, 'qtd': qtd})
    else:
        return redirect('inicio')

@login_required(login_url='login') 
def estoque(request):
    produtos = Produto.objects.all()
    return render(request, 'admins/estoque/index.html', {'produtos': produtos})

@login_required(login_url='login')
def carrinho(request):
    carrinhos = Carrinho.objects.filter(Q(usuario=request.user.id) & Q(status='A'))
    valor = 0
    produtos = []
    print()
    for carrinho in carrinhos:
        for prod in carrinho.produto.all():  # Preciso percorrer minha lista de produtos para somar a quantidade
            print(prod.id)
            hist_prod = None
            hist_prod = Hist_Produto.objects.get(usuario_id=request.user.id, produto_id=prod.id, carrinho='A')
            produtos.append(hist_prod)
            print('Quantidade')
            print(hist_prod.valor_uni * hist_prod.qtd)

            valor += hist_prod.valor_uni * hist_prod.qtd  # Precisa ser ajustado

        
    return render(request, 'clientes/carrinho/index.html', {'produtos': produtos, 'valor': valor})


def produto(request, id):
    produto = Produto.objects.get(id=id)
    categoria = Categoria.objects.raw(
        'select * from ecommerce_categoria limit 3')
    parcela = '{:.2f}'.format(produto.valor/12)
    return render(request, 'clientes/produto/index.html', {'produto': produto, 'parcela': parcela, 'categoria': categoria})


def categorias(request):
    categoria = Categoria.objects.raw(
        'select * from ecommerce_categoria limit 3')
    produtos = Produto.objects.all()
    return render(request, 'clientes/categorias/index.html', {'produtos': produtos, 'categoria': categoria})


def buscar(request):
    categoria = Categoria.objects.raw(
        'select * from ecommerce_categoria limit 3')
    busca = request.GET.get('pesquisa')
    produtos = Produto.objects.filter(
        Q(nome__icontains=busca) | Q(descricao__icontains=busca))
    return render(request, 'clientes/categorias/index.html', {'produtos': produtos, 'categoria': categoria})

@login_required(login_url='login')
def adicionaCart(request, id):
    user = request.user.id
    cart = Carrinho.objects.filter(usuario_id=user, status='A')
    pega_Produto = Produto.objects.get(id=id)
    if cart:
        cart = Carrinho.objects.get(usuario_id=user, status='A')
        cart.produto.add(pega_Produto)
        hist_prod = Hist_Produto.objects.filter(Q(usuario_id=user) & Q(produto_id=pega_Produto.id) & Q(carrinho='A'))

        if hist_prod:
            for prod in hist_prod:
                prod.qtd +=1
                prod.save()
        else:
            Hist_Produto.objects.create(produto_id=pega_Produto.id, valor_uni=pega_Produto.valor, qtd=1, usuario_id=user, movimentacao='E', carrinho='A')

    else:
        Hist_Produto.objects.create(produto_id=pega_Produto.id, valor_uni=pega_Produto.valor, qtd=1, usuario_id=user, movimentacao='E', carrinho='A')
        add_Carrinho = Carrinho.objects.create(usuario_id=user, status='A')
        add_Carrinho.produto.add(pega_Produto)

    return redirect(produto, id)
@login_required(login_url='login')
def comprar(request, id):
    user = request.user.id
    cart = Carrinho.objects.filter(usuario_id=user, status='A')
    pega_Produto = Produto.objects.get(id=id)
    if cart:
        cart = Carrinho.objects.get(usuario_id=user)
        cart.produto.add(pega_Produto)
        hist_prod = Hist_Produto.objects.filter(Q(usuario_id=user) & Q(produto_id=pega_Produto.id) & Q(carrinho='A'))

        if hist_prod:
            for prod in hist_prod:
                prod.qtd +=1
                prod.save()
        else:
            Hist_Produto.objects.create(produto_id=pega_Produto.id, valor_uni=pega_Produto.valor, qtd=1, usuario_id=user, movimentacao='E', carrinho='A')

    else:
        Hist_Produto.objects.create(produto_id=pega_Produto.id, valor_uni=pega_Produto.valor, qtd=1, usuario_id=user, movimentacao='E', carrinho='A')
        add_Carrinho = Carrinho.objects.create(usuario_id=user, status='A')
        add_Carrinho.produto.add(pega_Produto)   
    return redirect(carrinho)

@login_required(login_url='login')
def perfil(request):

    usuario = User.objects.get(id=request.user.id)
    print(usuario.first_name)
    if request.method == "POST":
        msg = ''
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        senha1 = request.POST.get('senha1').strip()
        senha2 = request.POST.get('senha2').strip()
        if first_name != usuario.first_name:
            usuario.first_name = first_name
            msg += "Usuario,"
        if last_name != usuario.last_name:
            usuario.last_name = last_name
            msg += "Ultimo Nome, "
        if email != usuario.email:
            usuario.email = email
            msg += "Email,"
        if senha1 == senha2 and senha1 != '' and senha2 != '':
            if len(senha1) <= 8 and len(senha1) >= 4:
                usuario.password = make_password(senha1)
                usuario.save()
                msg += "Senha,"
                return redirect('login')

            else:
                usuario.save()
        usuario.save()
        messages.success(request, msg + ' - Foram Salvos')
        return redirect('perfil')
    else:
        return render(request, 'clientes/perfil/index.html', {'usuario': usuario})

def sacs(request):
    return render(request, 'admins/sacs/index.html', {'sacs':Sac.objects.all()})
