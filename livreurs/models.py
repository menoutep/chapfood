from django.db import models
from base.models import Order

from accounts.models import CustomUser
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone
# Create your models here.
class DossierLivreur(models.Model):
    nom = models.CharField(max_length=255)
    prenoms = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.TextField()
    telephone = models.CharField(max_length=13, unique=True)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=255)
    nationalite = models.CharField(max_length=255)
    password1 = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255,unique=True)
    photo_livreur = models.ImageField(upload_to='dossier_livreurs/photo/%Y/%m/%d')
    permis_recto = models.ImageField(upload_to='dossier_livreurs/permis/%Y/%m/%d')
    permis_verso = models.ImageField(upload_to='dossier_livreurs/permis/%Y/%m/%d')
    carte_grise_recto = models.ImageField(upload_to='dossier_livreurs/carte_grise/%Y/%m/%d')
    carte_grise_verso = models.ImageField(upload_to='dossier_livreurs/carte_grise/%Y/%m/%d')
    assurance = models.ImageField(upload_to='dossier_livreurs/assurance/%Y/%m/%d')
    is_valid = models.BooleanField(default=False, editable=False)
    refuser = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom



class Livreur(User):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    dossier = models.OneToOneField(DossierLivreur, on_delete=models.CASCADE)
    position = models.TextField()
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.username 
    

STATUT_CHOICES = (
    ('en_attente', 'En attente'),
    ('en_cours', 'En cours'),
    ('livree', 'Livrée'),
    ('annulee', 'Annulée'),
)
   
class Livraison(models.Model):
    livreur = models.OneToOneField(Livreur, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Livraison {self.pk} ({self.status}) pour {self.livreur.dossier.nom} - Commande {self.order.pk}"





