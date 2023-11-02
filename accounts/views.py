

# Create your views here.
from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login
from livreurs.models import Livreur
from accounts.models import CustomUser
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserCreationForm, UserLoginForm




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




def custom_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigez l'utilisateur après une connexion réussie
                if Livreur.objects.filter(email=request.user.email).exists():
                    return redirect("livreurs:livreur-dashboard")
                elif CustomUser.objects.filter(email=request.user.email).exists():
                    # Rediriger l'utilisateur après une connexion réussie (par exemple, vers la page d'accueil)
                    return redirect('base:meal_list')
                else:
                    return redirect('base:index')  # Remplacez 'page_d_accueil' par le nom de votre vue d'accueil

    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('base:index')  # logout
