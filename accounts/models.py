from django.db import models

from django.contrib.auth.models import User

class CustomUser(User):
    phone_number = models.CharField(max_length=20)
    
    # Ajoutez d'autres champs personnalisés si nécessaire

    def __str__(self):
        return self.username