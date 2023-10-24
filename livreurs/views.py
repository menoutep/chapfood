from django.shortcuts import get_object_or_404, render, redirect
from .models import DossierLivreur,Livreur
from base.models import Order
from .forms import DossierCreationForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
# Create your views here.


def livreur_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Vérifiez si l'utilisateur est authentifié et s'il est une instance de la classe Livreur.
        if request.user.is_authenticated and isinstance(request.user, Livreur):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")
    return _wrapped_view
def is_superuser(user):
    return user.is_superuser

def index(request):
    return render(request, 'livreurs/index.html')

def depot_dossier(request):
    form = DossierCreationForm()
    if request.method == 'POST':
        form = DossierCreationForm(request.POST, request.FILES)
  
        if form.is_valid():
            # Créez une instance de Model3d à partir des données du formulaire
            form.save()
          
            return redirect('livreurs:index')  # Redirigez vers la page de détail du modèle 3D créé
    else:
        form = DossierCreationForm()
    return render(request, 'livreurs/depot_dossier.html',{'form': form})

@user_passes_test(is_superuser)
def dossier_attente(request):
    dossiers = DossierLivreur.objects.filter(is_valid=False)
    print(dossiers)
    context = {'dossiers':dossiers}
    return render(request, 'livreurs/dossier_attente.html',context)


@livreur_required
def livreur_dashboard(request):
    order = Order.objects.filter(waiting=True)
    context={"order":order}
    # Code de la vue accessible aux instances de la classe Livreur
    return render(request, 'livreur_dashboard.html',context)


@livreur_required
def accepter_commande(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    order.waiting = False
    order.save()
    return redirect('livreurs:livreur-dashboard')

@user_passes_test(is_superuser)
def valider_dossier_livreur(request, dossier_id):
    dossier = DossierLivreur.objects.get(id=dossier_id)
    dossier.is_valid = True
    dossier.save()
    if dossier.is_valid:
        # Créez un Livreur à partir des informations du dossier validé
        livreur = Livreur(
            username=dossier.username,
            email=dossier.email,
            password=make_password(dossier.password1),
            first_name=dossier.nom,
            last_name=dossier.prenoms,
            dossier=dossier,
            position="test",

            # Copiez d'autres champs du dossier ici
        )
        livreur.save()
         
        return redirect('livreurs:livreur-dashboard')  # Redirigez vers une page de confirmation
    else:
        return redirect('livreurs:dossiers-attente')

