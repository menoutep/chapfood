from django import forms
from .models import DossierLivreur
from datetime import datetime
from django.core.validators import validate_email,validate_image_file_extension, RegexValidator
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from .validators import validate_password, mail_is_unique, username_is_unique,validate_age
from django.core.exceptions import ValidationError

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',  # Modifiez cette regex en fonction de vos besoins
    message="Le numéro de téléphone doit être au format: '+999999999'. Il peut contenir jusqu'à 15 chiffres."
)
username_validator = UnicodeUsernameValidator()
class DossierCreationForm(forms.ModelForm):
    nom = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Entrez votre nom'})
        )
    prenoms = forms.CharField(
        max_length=255,
        label="Prénoms",
        widget=forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Entrez vos prenoms'})
        )
    adresse = forms.CharField(
        max_length=255,
        label="Adresse",
        widget=forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Entrez votre addresse'})
    )
    
    telephone = forms.CharField(
        max_length=13,
        label="télephone",
        widget=forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Entrez votre numéro de telephone'}),
        validators=[phone_regex],
        )
    
    date_naissance = forms.DateField(
        label = "date de naissance",
        widget=forms.DateInput(attrs={'class': 'form-control rounded', 'type': 'date','placeholder':'Entrez votre date de naissance'}),
        initial = "1960-01-01",
        help_text = "Vous devez avoir au moins 18 ans",
        validators=[validate_age]

    )
    lieu_naissance = forms.CharField(
        max_length=255,
        label="Lieu de naissance",
        widget=forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Entrez votre lieu de naissance'}),
        )
    nationalite = forms.CharField(
        max_length=255,
        label="Nationalité",
        widget=forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Entrez votre nationalité'}),
        help_text="ex : francaise",
        error_messages={"required": ("Ce champ est obligatoire")},
        )
    password1 = forms.CharField(
        max_length=60,
        min_length=8,
        widget=forms.PasswordInput(),
        label="Password1",
        help_text=("Doit contenir au moins 8 caractères et des chiffres"),
        validators=[validate_password],
        )
    password2 = forms.CharField(
        max_length=60,
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded','placeholder':'Confirmation du mot de passe'}),
        label="Password2",
        help_text=("Veuillez entrer le même mot de passe ci dessus."),
        validators=[validate_password],
    )
    email = forms.EmailField(
        label="Entrez votre email",
        widget=forms.EmailInput(attrs={'class': 'form-control rounded'}),
        validators=[validate_email,mail_is_unique] 
        )
    username = forms.CharField(
        max_length=150,
        min_length=4,
        label="Nom d'utilisateur",
        help_text="Minimum 4 caractères, maximum 150.",
        widget=forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Entrez votre nom username'}),
        validators=[username_validator,username_is_unique],

        )
    photo_livreur = forms.ImageField(
        label="photo",
        allow_empty_file= False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control rounded','placeholder':'Ajoutez une photo de vous'}),
        validators=[validate_image_file_extension]    
    )
    permis_recto = forms.ImageField(
        label="permis_recto",
        allow_empty_file= False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control rounded','placeholder':'Ajoutez une photo recto de votre permis de conduire'}),
        validators=[validate_image_file_extension]
        )
    permis_verso = forms.ImageField(
        label="permis_verso",
        allow_empty_file= False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control rounded','placeholder':'Ajoutez une photo verso de votre permis de conduire'}),
        validators=[validate_image_file_extension]
    )
    carte_grise_recto = forms.ImageField(
        label="carte grise recto",
        allow_empty_file= False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control rounded','placeholder':'Ajoutez une photo recto de votre carte grise'}),
        validators=[validate_image_file_extension]
        )
    carte_grise_verso = forms.ImageField(
        label="carte grise verso",
        allow_empty_file= False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control rounded','placeholder':'Ajoutez une photo verso de votre carte grise'}),
        validators=[validate_image_file_extension]
        )
    assurance = forms.ImageField(
        label="assurance",
        allow_empty_file= False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control rounded','placeholder':'Ajoutez une photo de votre assurance'}),
        validators=[validate_image_file_extension] 
    )
    class Meta:
        model = DossierLivreur
        fields='__all__' 
        exclude=['is_valid']
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get('password2')
        if password1 and password2:
            if not validate_password(password1):
                raise ValidationError(("Invalid value: %(value)s"),code="invalid",params={"value": password1},)
                #raise ValidationError("Le mot de passe doit contenir au moins 8 caractères et des chiffres.")
            elif password1 != password2:
                raise ValidationError("les mots de passes ne sont pas identiques.")
            
