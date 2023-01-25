from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
#from bands import urls


def register_account(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                form = UserCreationForm(initial={'username': request.POST['username']})
                return render(request, 'register.html', {'form': form,
                                                         'error': "Ce nom d'usager est déjà pris."})
        else:
            form = UserCreationForm(initial={'username': request.POST['username']})
            return render(request, 'register.html', {'form': form,
                                                     'error': 'Les mots de passe ne concordent pas.'})


def logout_account(request):
    logout(request)
    return redirect('home')


def login_account(request):
    if request.method == 'GET':
        return render(request, 'login.html',
                      {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'login.html',
                          {'form': AuthenticationForm(),
                           'error': 'Usage ou mot de passe invalide.'})
        else:
            login(request,user)
            return redirect('home')
