from django.shortcuts import get_object_or_404, render, redirect
from .models import DossierLivreur,Livreur, Livraison
from base.models import Order
from .forms import DossierCreationForm
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
# Create your views here.


def livreur_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Vérifiez si l'utilisateur est authentifié et s'il est une instance de la classe Livreur.
        if request.user.is_authenticated and Livreur.objects.filter(email=request.user.email).exists():
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



@livreur_required
def livreur_dashboard(request):
    orders = Order.objects.filter(status='en_cours',is_delivery=True)
    context={"orders":orders}
    # Code de la vue accessible aux instances de la classe Livreur
    return render(request, 'livreurs/livreur_dashboard.html',context)



@livreur_required
def accepter_livraison(request,order_id):
    livreur = Livreur.objects.get(email=request.user.email,username=request.user.username)
    order = Order.objects.get(id=order_id,status='en_cours',is_delivery=True)
    if order and livreur:
        order.status = "en_livraison"
        order.save()
        livraison = Livraison.objects.create(
            order=order,
            status="en_attente",
            livreur=livreur
        )
        livraison.save()  
        orders = Order.objects.filter(status='en_cours')
        response_data = {"orders":orders,"message":"livraison acceptée avec success"}
        return JsonResponse(response_data)
    else:
        response_data = {"error":"erreur d'acces ou erreur de validation"}
        return JsonResponse(response_data)
    
   
@livreur_required
def annuler_livraison(resquest,order_id):
    order = Order.objects.get(id=order_id,status='en_livraison',is_delivery=True)
    if order:
        order.status = "en_cours"
        order.save()
        livraison = Livraison.objects.get(order=order)
        livraison.delete()
        orders = Order.objects.filter(status='en_cours')
        response_data = {"orders":orders,"message":"annulation effectuée avec succes"}
        return JsonResponse(response_data)
    else:
        response_data = {"error":"erreur d'accès ou erreur de validation"}
        return JsonResponse(response_data)
@livreur_required
def start_livraison(order_id):
    order = Order.objects.get(id=order_id,status='en_livraison',is_delivery=True)
    livraison = Livraison.objects.get(order=order)
    if livraison:
        livraison.status = "en_cours"
        livraison.save()
        response_data = {"livraison":livraison}
        return JsonResponse(response_data)
    else:
        response_data = {"error":"erreur d'accés ou erreur de validation"}
        return JsonResponse(response_data)



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
         
        return redirect('livreurs:dossiers-attente')  # Redirigez vers une page de confirmation
    else:
        return redirect('livreurs:dossiers-attente')

@user_passes_test(is_superuser)
def dossier_attente(request):
    dossiers = DossierLivreur.objects.filter(is_valid=False)
    print(dossiers)
    
    context = {'dossiers':dossiers}
    return render(request, 'livreurs/dossier_attente.html',context)

@user_passes_test(is_superuser)
def accepter_commande(request,order_id):
    
    order = Order.objects.get(id=order_id,status='En attente')
    if order:
        order.status = "en_cours"
        order.save()
        orders = Order.objects.filter(status='En attente')
        response_data = {"orders":orders,"message":"Commande acceptée"}
        return JsonResponse(response_data)
    else:
        orders = Order.objects.filter(status='En attente')
        response_data = {"orders":orders,"message":"Erreur"}
        return JsonResponse(response_data)


   
