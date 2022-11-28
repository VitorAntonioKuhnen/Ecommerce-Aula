from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        check = auth.authenticate(request, username=usuario, password=senha)

        if check is not None:
            auth.login(request, check)

            if request.user.is_superuser:
                return redirect('dashboard')
            else:    
                return redirect('inicio')
        else:
            messages.error(request, 'Usuario ou Senha Incorreto!!')
            return redirect('login')
    else:
        return render(request, 'log_cad/index.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method == 'POST':
        primeiroNome = request.POST.get('primeiroNome').strip()
        ultimoNome = request.POST.get('ultimoNome').strip()
        email = request.POST.get('email').strip()
        usuario = request.POST.get('usuario').strip()
        senha = request.POST.get('senha')
        senha_2 = request.POST.get('comfirmaSenha')
        if len(primeiroNome) is not NULL:
            if len(ultimoNome) is not NULL:
                if len(email) is not NULL:
                    if len(usuario) >= 3:
                        if senha == senha_2:
                            if len(senha) >= 5 and len(senha) <= 12:
                                User.objects.create_user(
                                    username=usuario, password=senha, first_name=primeiroNome, last_name=ultimoNome, email=email)
                                return redirect('login')
                            else:
                                messages.error(
                                    request, 'Senha é menor que 5 ou maior que 12 caracteres!!')
                                return redirect('cadastro')
                        else:
                            messages.error(
                                request, 'Senha informadas são diferentes!!')
                            return redirect('cadastro')
                    else:
                        messages.error(
                            request, 'Usuario informado é menor que 3 caracters!!')
                        return redirect('cadastro')
                else:
                    messages.error(
                        request, 'É necessario informar um Email!!')
                    return redirect('cadastro')
            else:
                messages.error(
                    request, 'É necessario informar o Ultimo Nome!!')
                return redirect('cadastro')
        else:
            messages.error(
                request, 'É necessario informar o Primeiro Nome!!')
            return redirect('cadastro')
    else:
        return render(request, 'clientes/log_cad/index.html')
