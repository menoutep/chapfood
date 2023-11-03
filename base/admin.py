from django.contrib import admin
from .models import Category, Meal,Order,CartItem,CartItemMeal,PromoCode
from accounts.models import CustomUser
from livreurs.models import Livreur,DossierLivreur
# Register your models here.
admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(DossierLivreur)
admin.site.register(Livreur)
admin.site.register(CartItem)
admin.site.register(CartItemMeal)
admin.site.register(PromoCode)