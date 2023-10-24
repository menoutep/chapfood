from django.urls import path
from . import views

app_name='livreurs'
urlpatterns = [
    path('',views.index, name="index"),
    path('inscription/',views.depot_dossier, name="depot-dossiers"),
    path('attente_dossier/',views.dossier_attente, name="dossiers-attente"),
    path('livreur_dashboard/',views.livreur_dashboard, name="livreur-dashboard"),
    path('valider-dossier-livreur/<int:dossier_id>/', views.valider_dossier_livreur, name='valider-dossier-livreur'),
    #path('login/',views.login_view, name="login"),
    #path('logout/', views.logout_view, name='logout')

]