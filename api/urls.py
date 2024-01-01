from django.urls import path

from . import views
app_name='api'
urlpatterns = [
    
    path('auth-token/', views.index, name='api_view'),
    path('meal/<int:pk>', views.DetailApiView.as_view(), name='detail_api_view'),
    path('meal/create', views.CreateApiView.as_view(), name='create_api_view'),
    path('registration/', views.CustomUserRegistrationView.as_view(), name='api-registration'),
    path('cart/', views.cart, name='cart-view'),
    path('login/', views.login, name='api_view'),



    
]