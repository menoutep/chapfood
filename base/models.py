from django.db import models
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='meal_images/',blank=True, null=True)
    def get_meal_count(self):
        return Meal.objects.filter(category=self).count()
    def __str__(self):
        return self.name
    


class Meal(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    preparation_time = models.PositiveIntegerField(default=0, help_text="Temps de préparation en minutes")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.ImageField(upload_to='meal_images/')  # Champ pour l'image du repas

    def __str__(self):
        return self.name
    


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal, through='CartItemMeal')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def calculate_total(self):
        # Calculez le total en additionnant les prix des repas dans le panier
        total = sum(item.meal.price * item.quantity for item in self.cartitemmeal_set.all())
        self.total = total
        self.save()
        return self.total


    def __str__(self):
        return f"Panier de {self.user.username}"
    


class CartItemMeal(models.Model):
    cart_item = models.ForeignKey('CartItem', on_delete=models.CASCADE)
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Champ pour enregistrer la quantité de repas
    

    def calculate_item_total(self):
        # Calculez le prix total du repas en multipliant la quantité par le prix du repas
        return self.quantity * self.meal.price
        

    def __str__(self):
        return f"{self.quantity} x {self.meal.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItemMeal)  # Les repas commandés
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    is_delivery = models.BooleanField(default=False)  # True si le client souhaite être livré
    is_piece = models.BooleanField(default=False)
    monnaie = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    pickup_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commande de {self.user.username}"

    def calculate_order_total(self):
        total = sum(item.calculate_item_total() for item in self.items.all())
        if self.is_delivery:
            total += 500  # Ajoutez 500 au montant total si le client souhaite être livré
        return total

    # Ajoutez d'autres méthodes ou champs pour gérer l'état de la commande, la date de création, etc.






    




    

