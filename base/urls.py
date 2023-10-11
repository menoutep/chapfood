from django.urls import path

from . import views
app_name='base'
urlpatterns = [
    
    path('', views.meal_list, name='meal_list'),
    path('index/', views.index, name='index'),
    path('meals/<int:meal_id>/', views.meal_detail, name='meal_detail'),
    path('add_to_cart/<int:meal_id>/<int:quantity>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:meal_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/<int:meal_id>/<int:quantity>', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('meals/category/<int:category_id>/', views.meals_by_category, name='meals_by_category'),

]