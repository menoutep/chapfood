from django.urls import path

from . import views
app_name='api'
urlpatterns = [
    
    path('meal/', views.index, name='api_view'),
    path('meal/<int:pk>', views.DetailApiView.as_view(), name='detail_api_view'),
    path('meal/create', views.CreateApiView.as_view(), name='create_api_view'),

    
]