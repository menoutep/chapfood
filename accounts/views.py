

# Create your views here.
from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login

from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserCreationForm




# Dans accounts/views.py
def SignUpView(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authentifiez l'utilisateur
            user = authenticate(request, username=username, password=password)
            # Connectez automatiquement l'utilisateur
            login(request, user)
            return redirect('base:meal_list')
            
    else:
        form=UserCreationForm()
        
    context={
        'form':form,
    }
    return render(request,'accounts/signup.html',context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Rediriger l'utilisateur après une connexion réussie (par exemple, vers la page d'accueil)
            return redirect('base:meal_list')
        else:
            # Authentification échouée, renvoyer un message d'erreur à l'utilisateur
            return render(request, 'accounts/login.html', {'error_message': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('base:index')  # logout
