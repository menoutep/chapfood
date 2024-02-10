#!/bin/bash

# Vérifier si un message de commit a été fourni en argument
if [ -z "$1" ]; then
    echo "Veuillez fournir un message de commit en argument."
    exit 1
fi

# Ajouter tous les fichiers au suivi de Git
git add .

# Effectuer le commit avec le message fourni en argument
git commit -m "$1"

# Afficher un message de confirmation
echo "Le commit a été effectué avec succès."

# Effectuer un push vers le dépôt distant (changez 'origin' et 'master' selon vos besoins)
git push origin prod

# Afficher un message de confirmation pour le push
echo "Le code a été poussé vers le dépôt distant (GitHub)."
