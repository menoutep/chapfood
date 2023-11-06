from django.shortcuts import get_object_or_404, render, redirect
from .models import DossierLivreur,Livreur, Livraison
from base.models import Order
from .forms import DossierCreationForm
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
# Create your views here.

####################################utils#######################
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

def livreur_disponible(livreur):
    """Retourne True si le livreur est disponible."""
    if livreur.status == 'en_attente':
        if livreur.livraison_count <=3:    
            return True
        else:    
            return False
    elif livreur.status == 'en_livraison':
        if livreur.livraison_count <=2:
            return True
        else:
            return False
        

####################################fin utils#######################
######################################livreur view#########################
def index(request):
    return render(request, 'livreurs/index.html')

def depot_dossier(request):
    form = DossierCreationForm()
    if request.method == 'POST':
        form = DossierCreationForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid():
            # Créez une instance de Model3d à partir des données du formulaire
            
            form.save()
          
            return redirect('base:index')  # Redirigez vers la page de détail du modèle 3D créé
        else:
            print(form.errors)
    else:
        
        form = DossierCreationForm()
    return render(request, 'livreurs/depot_dossier.html',{'form': form})



@livreur_required
def livreur_dashboard(request):
    livreur = Livreur.objects.get(email=request.user.email,username=request.user.username)
    livraisons_en_cours = Livraison.objects.filter(status="en_cours",livreur=livreur)
    orders = Order.objects.filter(status='en_cours',is_delivery=True)
    print(livreur.livraison_count)
    print(livreur.status)
    print(livreur_disponible(livreur=livreur))
    if livraisons_en_cours and len(livraisons_en_cours)>0:
        context={"orders":orders,"livraisons_en_cours":livraisons_en_cours}
    else :
        context={"orders":orders}
    # Code de la vue accessible aux instances de la classe Livreur
    return render(request, 'livreurs/livreur_dashboard.html',context)



@livreur_required
def accepter_livraison(request,order_id):  
    print("pb") 
    livreur = Livreur.objects.get(email=request.user.email,username=request.user.username)
    order = Order.objects.get(id=order_id,status='en_cours',is_delivery=True)
    active = livreur_disponible(livreur=livreur)
    print(active)
    print("pb")
    if order:       
        if active:
            print(livreur.is_active)
            order.status = "en_livraison"
            order.save()
            livraison = Livraison.objects.create(
                order=order,
                status="en_attente",
                livreur=livreur
            )
            livraison.save()

            livreur.livraison_count = livreur.livraison_count + 1
            print(livreur.livraison_count)
            livreur.save()
            orders = Order.objects.filter(status='en_cours')
            response_data = {"livraison_position":livraison.order.delivery_address,"livraison_status":livraison.status,"message":"livraison acceptée avec success"}
            return JsonResponse(response_data)
        else :
            response_data = {"error":"error"}
            print("nice my son")
            return JsonResponse(response_data)
    else:
        response_data = {"error":"erreur d'acces ou erreur de validation"}
        return JsonResponse(response_data)
@livreur_required
def detail_livraison(request):
    #trouver un moyen de trier les livraison prise lorsque le livreur est en attente de celle lorsque le livreur est en course 
    livreur = Livreur.objects.get(email=request.user.email,username=request.user.username)
    
    livraisons = Livraison.objects.filter(Q(status='en_attente') | Q(status='en_cours'),livreur=livreur)
    print(livraisons)
    address_list = {}
    
    if livraisons :
        for livraison in livraisons:
            address_list[livraison.order.user.username]=livraison.order.delivery_address
        response_data = {"address_list":address_list,"livraison_status":livraison.status,"message":"livraison acceptée avec success"}
        return JsonResponse(response_data)
    else: 
        response_data = {"message":"vous n'avez pas de livraison en cours veuillez en selectionner une "}
        return JsonResponse(response_data)
   
@livreur_required
def annuler_livraison(request,order_id):
    livreur = Livreur.objects.get(email=request.user.email,username=request.user.username)
    order = Order.objects.get(id=order_id,status='en_livraison',is_delivery=True)
    if order:
        order.status = "en_cours"
        order.save()
        livraison = Livraison.objects.get(order=order,livreur=livreur)
        livraison.delete()
        livreur.livraison_count -=1
        livreur.save()
        orders = Order.objects.filter(status='en_cours')
        response_data = {"message":"annulation effectuée avec succes"}
        return JsonResponse(response_data)
    else:
        response_data = {"error":"erreur d'accès ou erreur de validation"}
        return JsonResponse(response_data)
@livreur_required
def start_livraison(request):
    livreur = Livreur.objects.get(email=request.user.email,username=request.user.username)
  
    livraisons = Livraison.objects.filter(status='en_attente',livreur=livreur)
    if livraisons and len(livraisons)>0:
        for livraison in livraisons:
            if livraison:
                livraison.status = "en_cours"
                livraison.save()

        livreur.status = "en_livraison"
        livreur.save()
        
        response_data = {"message":"message_start"}
        return JsonResponse(response_data)
    else:
        response_data = {"error":"erreur d'accés ou erreur de validation"}
        return JsonResponse(response_data)
    
@livreur_required
def end_livraison(request,livraison_id):
    livreur = Livreur.objects.get(email=request.user.email,username=request.user.username)
    livraison = Livraison.objects.get(id=livraison_id,livreur=livreur)
    if livraison:
        livraison.status = 'livree'
        livraison.save()
        livreur.livraison_count -=1
        if livreur.livraison_count == 0:
            livreur.status = 'en_attente'
        livreur.save()
        
        response_data = {"message":"livraison terminer"}
        return JsonResponse(response_data)
    else:
        response_data = {"error":"erreur d'accés ou erreur de validation"}
        return JsonResponse(response_data)

################################end livreur view#######################################

################################################ADMIN#######################################################
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
         
        return redirect('livreurs:admin_dashboard')  # Redirigez vers une page de confirmation
    else:
        return redirect('livreurs:admin_dashboard')
    
@user_passes_test(is_superuser)
def dossier_detail(request, dossier_id):
    dossier = DossierLivreur.objects.get(pk=dossier_id)
    
    # Récupérez trois repas de la même catégorie, en excluant le repas actuel
    
    return render(request, 'livreurs/dossier_detail.html', {'dossier': dossier})
@user_passes_test(is_superuser)
def refuser_dossier(request, dossier_id):
    dossier = DossierLivreur.objects.get(id=dossier_id,refuser=False)
    dossier.refuser = True
    dossier.save()
    
    # Récupérez trois repas de la même catégorie, en excluant le repas actuel
    
    return redirect('livreurs:admin_dashboard')

@user_passes_test(is_superuser)
def admin_dashboard(request):
    dossiers = DossierLivreur.objects.filter(is_valid=False,refuser=False)
    orders = Order.objects.filter(status='en_attente')
    print(dossiers)
    print(orders)
    
    context = {'dossiers':dossiers,'orders':orders}
    return render(request, 'livreurs/admin_dashboard.html',context)

@user_passes_test(is_superuser)
def accepter_commande(request,order_id):
    
    order = Order.objects.get(id=order_id,status='en_attente')
    if order:
        order.status = "en_cours"
        order.save()
        orders = Order.objects.filter(status='en_attente')
        response_data = {"message":"Commande acceptée"}
        return JsonResponse(response_data)
    else:
        orders = Order.objects.filter(status='en_attente')
        response_data = {"message":"Erreur"}
        return JsonResponse(response_data)


   
