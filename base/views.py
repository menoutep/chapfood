from django.shortcuts import render, redirect
from .models import Meal, CartItem, CartItemMeal,Category,PromoCode
from .forms import MealForm,ContactForm
from django.contrib.auth.decorators import login_required
from .forms import DeliveryForm
from .models import Order
from api.serializers import OrderSerializer
from accounts.models import CustomUser
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
# Create your views here.
from livreurs.models import Livreur
import json

# Fonction pour envoyer le nombre d'éléments du panier
def send_cart_item_count_to_clients(item_count):
    # Récupère la couche de canal
    channel_layer = get_channel_layer()

    # Envoie le nombre d'éléments du panier aux clients connectés
    async_to_sync(channel_layer.group_send)(
        "notifications_type4",
        {
            "type": "send_notification_type4",
            "message": item_count
        }
                
    )

def customer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Vérifiez si l'utilisateur est authentifié et s'il est une instance de la classe Livreur.
        if request.user.is_authenticated and CustomUser.objects.filter(email=request.user.email,username=request.user.username).exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")
    return _wrapped_view



@login_required
def index(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    categories=Category.objects.all()
    for cat in categories:
        cat.is_active()
        print(cat.active)
    
    meals=Meal.objects.filter(Q(name__icontains=q) |
                              Q(category__name__icontains=q) |          
                              Q(description__icontains=q),category__active=True)
    

    if meals.count() == 0:
        meals = meals=Meal.objects.filter(Q(name__icontains=q) |
                              Q(category__name__icontains=q) |          
                              Q(description__icontains=q)) 
    
    cheapest_meal = meals.order_by('price').first()
    
    if CustomUser.objects.filter(username=request.user.username).exists() and CartItem.objects.filter(user__username=request.user.username,last=True).exists() :
        customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
        cart = CartItem.objects.get(user=customer,last=True)
        quantite_panier = cart.quantity_sum

        context={
            'categories':categories,
            'meals':meals,
            'cheapest_meal':cheapest_meal,
            'quantite_panier':quantite_panier
        }
        return render(request, 'base/index_.html',context)
    else :
        context={
            'categories':categories,
            'meals':meals,
            'cheapest_meal':cheapest_meal,
            
        }
        return render(request, 'base/index.html',context)

@login_required
def meal_list(request):
    categories=Category.objects.all()
    for cat in categories:
        cat.is_active()
        print(cat.active)
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    meals=Meal.objects.filter(Q(name__icontains=q) |
                              Q(category__name__icontains=q) | 
                              Q(description__icontains=q),category__active=True)
    categories=Category.objects.filter(Q(name__icontains=q) | Q(description__icontains=q),active=True)

    cheapest_meal = meals.order_by('price').first()

    if CustomUser.objects.filter(username=request.user.username).exists() and CartItem.objects.filter(user__username=request.user.username,last=True).exists() :
        customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
        cart = CartItem.objects.get(user=customer,last=True)
        quantite_panier = cart.quantity_sum
        context={
        'categories':categories,
        'meals':meals,
        'cheapest_meal':cheapest_meal,
        'quantite_panier':quantite_panier,
        }
        return render(request, 'base/meal_list_.html',context)
    else:
        context={
            'categories':categories,
            'meals':meals,
            'cheapest_meal':cheapest_meal
        }
        return render(request, 'base/meal_list.html',context)

@login_required
def meals_by_category(request, category_id):
    # Récupérez la catégorie en fonction de l'ID
    category = Category.objects.get(id=category_id)
    
    # Récupérez les repas appartenant à cette catégorie
    meals = Meal.objects.filter(category=category)
    cheapest_meal = Meal.objects.all().order_by('price').first()
    if CustomUser.objects.filter(username=request.user.username).exists() and CartItem.objects.filter(user__username=request.user.username,last=True).exists() :
        customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
        cart = CartItem.objects.get(user=customer,last=True)
        quantite_panier = cart.quantity_sum
        context={
        'category':category,
        'meals':meals,
        'cheapest_meal':cheapest_meal,
        'quantite_panier':quantite_panier,
        }
        return render(request, 'base/meals_by_category_.html', context)
    else:
        context = {
            'category': category, 
            'meals': meals,
            'cheapest_meal':cheapest_meal,
                }
        return render(request, 'base/meals_by_category.html', context)


def contact(request):
    form = ContactForm() 
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            email=form.cleaned_data["email"]
            phone=form.cleaned_data["phone"]
            message=form.cleaned_data["message"]
            subject=form.cleaned_data["subject"]
            subject = f'Message contact de {name} au sujet de {subject}'
            message += f"le numero de l'utilisateur est {phone}:\n\n"
            message += f'le message est : {message},\n\n'
            from_email = 'jozacoder@gmail.com'  # Remplacez par votre adresse e-mail
            recipient_list = ['josephzabre@gmail.com']  # Adresse e-mail du destinataire (utilisateur)            
            send_mail(subject, message, from_email, recipient_list)
        else:
            form = ContactForm()
    return render(request, 'base/contact.html',{'form': form})

def about(request):
    return render(request, 'base/about.html')


def meal_detail(request, meal_id):
    meal = Meal.objects.get(pk=meal_id)
    category = meal.category

    # Récupérez trois repas de la même catégorie, en excluant le repas actuel
    similar_meals = Meal.objects.filter(category=category).exclude(pk=meal_id)[:3]
    if CustomUser.objects.filter(username=request.user.username).exists() and CartItem.objects.filter(user__username=request.user.username,last=True).exists() :
        customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
        cart = CartItem.objects.get(user=customer,last=True)
        quantite_panier = cart.quantity_sum
        context = {
        'meal': meal,
        'similar_meals':similar_meals,
        'quantite_panier': quantite_panier,
        }
        return render(request, 'base/meal_detail_.html', context)
    else :
        context = {
            'meal': meal,
            'similar_meals':similar_meals
            }
        return render(request, 'base/meal_detail.html', context)


@customer_required
def add_to_cart(request, meal_id,quantity):
    
    try:
        meal = Meal.objects.get(id=meal_id)
    except Meal.DoesNotExist:
        # Gérer le cas où le repas n'existe pas
        return redirect('base:meal_list')  # Rediriger vers la liste des repas ou une autre vue appropriée
    # Vérifier si l'utilisateur a déjà un panier, sinon, créez-en un
    customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
    cart, created_ = CartItem.objects.get_or_create(user=customer,last=True)
    
    # Vérifier si le repas est déjà dans le panier de l'utilisateur
    cart_item_meal, created = CartItemMeal.objects.get_or_create(cart_item=cart, meal=meal)

    # Augmenter la quantité si le repas est déjà dans le panier, sinon, l'ajouter au panier
    if not created:
        if quantity == 0:
            cart_item_meal.quantity += 1
            cart_item_meal.save()
        elif quantity >= 1:
            cart_item_meal.quantity = quantity
            cart_item_meal.save()


    # Calculer le total du panier
    cart.calculate_total()
    send_cart_item_count_to_clients(cart.quantity_sum)
    # Rediriger l'utilisateur vers la liste des repas ou une autre vue appropriée
    return redirect('base:meal_list')

@customer_required
def cart(request):
    customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
    # Récupérez le panier de l'utilisateur connecté
    cart, created = CartItem.objects.get_or_create(user=customer,last=True)
    quantite_panier = cart.quantity_sum
    total = cart.calculate_total()
    code_promo= request.GET.get('code_promo')
    print(code_promo)
    ancien_total = 0
    if code_promo:
        ancien_total = total
        if isinstance(code_promo, str):
            promo = PromoCode.objects.get(code=code_promo)
            promo.is_active()
            print(promo.active)
            if promo and promo.active:
                print(promo.discount_type)
                if promo.discount_type=='percent':
                    discount = (total * promo.discount_value)/100
                    cart.total = total-discount
                    cart.save()
                    promo.active = False
                    promo.save()


                elif promo.discount_type == 'amount':
                    discount = promo.discount_value
                    cart.total = total - discount
                    cart.save()
                    promo.active = False
                    promo.save()

    


    # Calculer le prix total du panier en parcourant les repas dans le panier
    
    
    context = {'cart': cart, 'total': cart.total,'ancien_total':ancien_total,'quantite_panier':quantite_panier}
    
    return render(request, 'base/cart.html', context)


@customer_required
def update_cart(request, meal_id,quantity):
    try:
        customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
        cart_item_meal = CartItemMeal.objects.get(cart_item__user=customer, meal__id=meal_id,cart_item__last=True)
    except CartItemMeal.DoesNotExist:
        # Gérer le cas où le repas n'est pas dans le panier
        return redirect('base:cart')  # Rediriger vers le panier ou une autre vue appropriée 
    if quantity >= 1:
        cart_item_meal.quantity = quantity
        cart_item_meal.save()
        cart_item_meal_total = cart_item_meal.calculate_item_total()
        customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
        cart = CartItem.objects.get(user=customer,last=True)
        cart_total = cart.calculate_total()
        send_cart_item_count_to_clients(cart.quantity_sum)
        response_data = {'message': 'Quantité mise à jour avec succès', 'new_quantity': cart_item_meal.quantity, 'item_total':cart_item_meal_total,'cart_total':cart_total}
    redirect('base:cart')
    return JsonResponse(response_data)

@customer_required
def remove_from_cart(request, meal_id):
    customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
    try:
        cart_item_meal = CartItemMeal.objects.get(cart_item__user=customer, meal__id=meal_id,cart_item__last=True)
        cart_item_meal.delete()
    except CartItemMeal.DoesNotExist:
        # Gérer le cas où le repas n'est pas dans le panier
        pass

    cart = CartItem.objects.get(user=customer,last=True)
    cart_total = cart.calculate_total()
    send_cart_item_count_to_clients(cart.quantity_sum)
    response_data = {'message': 'Quantité mise à jour avec succès','cart_total':cart_total}
    redirect('base:cart')
    
    return JsonResponse(response_data)


@customer_required
def checkout(request):
    
    customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
    # Récupérez le panier de l'utilisateur connecté
    cart = CartItem.objects.get(user=customer,last=True)
    quantite_panier = cart.quantity_sum
    print(f"quantity : {cart.quantity_sum}")
    time_cook = max(item.meal.preparation_time for item in cart.cartitemmeal_set.all())
    # Vérifiez si le formulaire de livraison a été soumis
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            # Enregistrez les informations de livraison dans la commande
            delivery_address = form.cleaned_data['delivery_address']
            is_delivery = form.cleaned_data['is_delivery']
            monnaie = form.cleaned_data['monnaie']
            is_piece = form.cleaned_data['is_piece']
            
            if is_delivery:
            # Calculez le montant total de la commande en utilisant la méthode du modèle Order
                order_total = cart.total + 500
            else:
                order_total = cart.total

            
            # Créez une nouvelle commande sans le champ order_total
            order = Order.objects.create(
                user=customer,
                delivery_address=delivery_address,
                is_delivery=is_delivery,
                is_piece=is_piece,
                monnaie=monnaie,
                time_cook=time_cook,
                order_total=order_total,       
            )
            
            # Ajoutez les repas du panier à la commande
            order.items.set(cart.cartitemmeal_set.all())
            order.save()  
            serializer = OrderSerializer(order)
            serialized_data = serializer.data
            print(serialized_data)
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications_type1",
                {
                    "type": "send_notification_type1",
                    "message": serialized_data
                }
            )
            
            send_order_email(order,subject=None)
            # Vider le panier
            #cart.cartitemmeal_set.all().delete()
            cart.last=False
            cart.save()
            # Redirigez vers une page de succès de la commande
            return redirect('base:order_success')
    else:
        form = DeliveryForm()
    
    context = {'cart': cart, 'form': form,'order_total': cart.total,'quantite_panier':quantite_panier}
    return render(request, 'base/checkout.html', context)


@customer_required
def order_success(request):
    customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
    last_order = Order.objects.filter(user=customer).latest('created_at')
    
    # Vous pouvez ajouter du contexte ici si nécessaire
    return render(request, 'base/order_success.html')


@customer_required
def send_order_email(order,subject):
    # Créez le contenu de l'e-mail
    
    customer = CustomUser.objects.get(username=order.user.username,email=order.user.email)
    phone_number = customer.phone_number

    if subject : 
        message = f"Une nouvelle livraison est en attente\n"
        subject = 'Nouvelle livraison\n'
        livreurs_mails = [livreur.email for livreur in Livreur.objects.all()]
        recipient_list = livreurs_mails   # Ajoutez les adress

    else : 
        subject = 'Confirmation de commande\n'
        message = f"Bonjour ChapFood,\n"
        recipient_list = ['josephzabre@gmail.com']

    message += f"Vous avez une commande de {order.user.username}.\nContact : {phone_number}.\n Voici un récapitulatif de sa commande :\n\n"

    for item in order.items.all():
        message += f"{item.meal.name} x{item.quantity}: {item.calculate_item_total()} cfa\n"
    
    message += f"Total de la commande : {order.order_total} cfa\n"
    
    if order.is_delivery:
        message += f"Livraison à l'adresse suivante : {order.delivery_address}. \n"
        
    else:
        message += f"heure de récupération : {order.pickup_time}. \n"
    if order.is_piece:
        message += "Le client a la monnaie exacte. \n"
    else:
        message += f"Le client n'a pas la monnaie il a : {order.monnaie}. \n"
    # Envoyez l'e-mail
    from_email = 'jozacoder@gmail.com'  # Remplacez par votre adresse e-mail
    
      # Adresse e-mail du destinataire (utilisateur)

    send_mail(subject, message, from_email, recipient_list)


    


