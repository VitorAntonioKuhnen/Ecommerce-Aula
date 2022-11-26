from django.shortcuts import render, redirect
from django.contrib import auth, messages

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        check = auth.authenticate(request, username=usuario, password=senha)

        if check is not None:
            auth.login(request, check)
            print(check)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario ou Senha Incorreto!!')
            return redirect('login')
    else:
        return render(request, 'login/index.html')
