from django.db import models
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import datetime
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='meal_images/',blank=True, null=True)
    start_time = models.TimeField(help_text="Date de début de validité du code promotionnel",null=True,blank=True)
    end_time = models.TimeField(help_text="Date de fin de validité du code promotionnel",null=True,blank=True)
    active = models.BooleanField(default=False, help_text="Code promotionnel actif ou inactif")
    
    
    def is_active(self):
        """
        Vérifie si la categorie est active en fonction de l'heure actuelle.
        """
        if self.start_time and self.end_time:
            now = datetime.now().time()
            if self.start_time <= now <= self.end_time:
                self.active = True
            else:
                self.active = False
            self.save()  
        else:
            self.active = True
            self.save() 

    def get_meal_count(self):
        return Meal.objects.filter(category=self).count()
    def __str__(self):
        return self.name
    


class Meal(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_promo = models.BooleanField(default=False)
    preparation_time = models.PositiveIntegerField(default=0, help_text="Temps de préparation en minutes")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    second_price = models.DecimalField(max_digits=15,default=0,decimal_places=2)
    image = models.ImageField(upload_to='meal_images/')  # Champ pour l'image du repas

    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal, through='CartItemMeal')
    last = models.BooleanField(null=False,default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

      # Importez le type Decimal

    def calculate_total(self):
        total = Decimal('0.0')  # Initialisez le total en tant que Decimal

        for cart_item in self.cartitemmeal_set.all():
            meal = cart_item.meal
            if meal.is_promo:
                # Si l'article est en promotion, utilisez second_price
                total += meal.second_price * Decimal(cart_item.quantity)
            else:
                # Sinon, utilisez le prix normal
                total += meal.price * Decimal(cart_item.quantity)

        self.total = total
        self.save()
        return self.total
    @property
    def quantity_sum(self):
        """Retourne la somme des quantités d'articles dans ce panier"""
        qty_sum = sum([i.quantity for i in self.cartitemmeal_set.all()])
        return qty_sum

    def __str__(self):
        return f"Panier de {self.user.username}"
        


class CartItemMeal(models.Model):
    cart_item = models.ForeignKey('CartItem', on_delete=models.CASCADE)
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Champ pour enregistrer la quantité de repas
    
    def calculate_item_total(self):
        # Calculez le prix total du repas en multipliant la quantité par le prix du repas
        total = Decimal('0.0')
        if self.meal.is_promo:
            total = self.meal.second_price * Decimal(self.quantity)
            return total
        else:
            total = self.meal.price * Decimal(self.quantity)
            return total
    
    def __str__(self):
        return f"{self.quantity} x {self.meal.name}"
   
STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de préparation'),
        ('en_livraison', 'En cours de livraison'),
        ('livree', 'Livrée'),
        ('recuperer', 'Récupérée'),
        ('annulee', 'Annulée'),
    )   
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItemMeal)  # Les repas commandés
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    is_delivery = models.BooleanField(default=False)  # True si le client souhaite être livré
    is_piece = models.BooleanField(default=False)
    monnaie = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    pickup_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    time_cook = models.PositiveIntegerField(default=0)

    
    def __str__(self):
       
        return f"Commande de {self.user.username}"
    
    def calculate_order_total(self):
        total = sum(item.calculate_item_total() for item in self.items.all())
        if self.is_delivery:
            total += 500  # Ajoutez 500 au montant total si le client souhaite être livré
        return total
    


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, help_text="Code promotionnel unique")
    description = models.TextField(max_length=200, help_text="Description du code promotionnel")
    discount_type = models.CharField(
        max_length=60,
        choices=[('percent', 'Pourcentage'), ('amount', 'Montant fixe')],
        default='percent',
        help_text="Type de réduction (pourcentage ou montant fixe)"
    )
    discount_value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        help_text="Montant de la réduction en pourcentage (0-100) ou montant fixe"
    )
    start_date = models.DateTimeField(help_text="Date de début de validité du code promotionnel")
    end_date = models.DateTimeField(help_text="Date de fin de validité du code promotionnel")
    active = models.BooleanField(default=False, help_text="Code promotionnel actif ou inactif")

    def __str__(self):
        return self.code
    
    def is_active(self):
        """
        Vérifie si le code promotionnel est actif en fonction de la date actuelle.
        """
        now = timezone.now()
        if self.start_date <= now <= self.end_date:
            self.active = True
        else:
            self.active = False
        self.save()  # Enregistrez la modification de la valeur act





    




    

