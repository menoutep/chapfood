from django.urls import path
from . import views

app_name='livreurs'
urlpatterns = [
    path('',views.index, name="index"),
    path('inscription/',views.depot_dossier, name="depot-dossiers"),
    path('admin_dashboard/',views.admin_dashboard, name="admin_dashboard"),
    path('livreur_dashboard/',views.livreur_dashboard, name="livreur-dashboard"),
    path('valider-dossier-livreur/<int:dossier_id>/', views.valider_dossier_livreur, name='valider-dossier-livreur'),
    path('accepter_commande/<int:order_id>/', views.accepter_commande, name='accepter-commande'),
    path('dossier_detail/<int:dossier_id>/', views.dossier_detail, name='dossier-detail'),
    path('refuser_dossier/<int:dossier_id>/', views.refuser_dossier, name='refuser-dossier'),
    path('accepter_livraison/<int:order_id>/', views.accepter_livraison, name='accepter-livraison'),
    path('annule_livraison/<int:order_id>/', views.annuler_livraison, name='annuler-livraison'),
    path('detail_livraison/', views.detail_livraison, name='detail-livraison'),
    path('start_livraison/<int:order_id>/', views.start_livraison, name='start-livraison'),
    path('end_livraison/<int:livraison_id>/', views.end_livraison, name='end-livraison'),

]

