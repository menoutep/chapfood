from django.contrib import admin
from .models import Category, Meal,Order
from accounts.models import CustomUser
# Register your models here.
admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(CustomUser)
admin.site.register(Order)
