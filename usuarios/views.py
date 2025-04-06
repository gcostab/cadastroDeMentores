from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senha e confirmar senha devem ser iguais.')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve ter no mínimo 6 caracteres.')
            return redirect('/usuarios/cadastro')

        users = User.objects.filter(username=username)
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuario com esse username.')
            return redirect('/usuarios/cadastro')

        User.objects.create_user(
            username=username,
            password=senha
        )    

        return redirect('/usuarios/login')
    
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/mentorados/')
        
        messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
        return redirect('login')