# Dans accounts/forms.py
from django import forms
from django.contrib.auth import password_validation

from django.core.validators import validate_email, RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm,PasswordChangeForm,SetPasswordForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Submit, ButtonHolder
from livreurs.forms import username_is_unique,username_validator,validate_password,mail_is_unique
from django.core.exceptions import ValidationError

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',  # Modifiez cette regex en fonction de vos besoins
    message="Le numéro de téléphone doit être au format: '+999999999'. Il peut contenir jusqu'à 15 chiffres."
)
username_validator = UnicodeUsernameValidator()

class UserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        min_length=4,
        label="Nom d'utilisateur",
        help_text="Minimum 4 caractères, maximum 150.",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Entrez votre nom username'}),
        validators=[username_validator,username_is_unique],
        )
    email = forms.EmailField(
        label="email",
        help_text="adresse mail active",
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Entrez votre nom email'}),
        validators=[validate_email,mail_is_unique] 
        )
    phone_number = forms.CharField(
        max_length=13,
        label="télephone",
        help_text="format : +2250667897876",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Entrez votre numéro de telephone'}),
        validators=[phone_regex],
        )
    password1 = forms.CharField(
        max_length=60,
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Entrez votre mot de passe'}),
        label="Password1",
        help_text=("Doit contenir au moins 8 caractères et des chiffres"),
        validators=[validate_password],
        )
    password2 = forms.CharField(
        max_length=60,
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmation du mot de passe'}),
        label="Password2",
        help_text=("Veuillez entrer le même mot de passe ci dessus."),
        validators=[validate_password],
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

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

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # Méthode du formulaire (post par défaut)
        self.helper.form_class = 'my-form'  # Classe CSS pour le formulaire
        self.helper.form_show_labels = True  # Afficher les étiquettes des champs
        self.helper.form_show_errors =True
        self.helper.label_class = 'col-sm-3 col-form-label'
        self.helper.field_class = 'col-sm-8'
        self.helper._help_text_inline = True
        self.helper.layout = Layout(
            
            Field('username',css_class='col-md-9'),
            Field('email',css_class='col-md-9'),
            Field('phone_number',css_class='col-md-9'),
            Field('password1',css_class='col-md-9'),
            
            Field('password2',css_class='col-md-9'),
            Submit('submit', "S'enregistrer", css_class='btn btn-primary')
        )




class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # Méthode du formulaire (post par défaut)
        self.helper.form_class = 'my-login-form'  # Classe CSS pour le formulaire

        self.helper.layout = Layout(
            
            Field('username',css_class='col-md-9'),
            
            Field('password',css_class='col-md-9'),
            Submit('submit', 'Se connecter', css_class='btn btn-primary')
        )

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label = 'email',
        help_text="entrez l'adresse email avec laquelle vous vous etes inscrit",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Votre adresse mail'})
        )
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # Méthode du formulaire (post par défaut)
        self.helper.form_class = 'my-login-form'  # Classe CSS pour le formulaire
        self.helper.form_show_labels = True  # Afficher les étiquettes des champs
        self.helper.form_show_errors =True
        self.helper._help_text_inline = True
        self.helper.layout = Layout(
            
            Field('email',css_class='col-md-9'),
            
            Submit('submit',"Réinitialiser mon mot de passse", css_class='btn btn-primary')
            
        )
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Ancien mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "mot de passe actuel", "autofocus": True,'class':'form-control','placeholder':'Entrez votre ancien mot de passe'}
        ),
    )
    new_password1 = forms.CharField(
        label=("Nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={"autocomplete": "nouveau-mot de passe",'class':'form-control','placeholder':'Entrez votre mot de passe'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Nouveau mot de passe confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "Nouveau mot de passe",'class':'form-control','placeholder':'Confirmation du mot de passe'}),
    )
    field_order = ["old_password", "new_password1", "new_password2"]

    def __init__(self,*args, **kwargs):
        
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # Méthode du formulaire (post par défaut)
        self.helper.form_class = 'my-login-form'  # Classe CSS pour le formulaire
        self.helper.form_show_labels = True  # Afficher les étiquettes des champs
        self.helper.form_show_errors =True
        self.helper._help_text_inline = True
        self.helper.layout = Layout(
            
            Field('old_password',css_class='col-md-9'),
            Field('new_password1',css_class='col-md-9'),
            Field('new_password2',css_class='col-md-9'),
            Submit('submit',"Réinitialiser mon mot de passse", css_class='btn btn-primary')
            
        )

class SetPasswordForm(SetPasswordForm):
    """
    A form that lets a user set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch":("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=("Nouveau mot de passe"),
        widget=forms.PasswordInput(attrs={"autocomplete": "nouveau-mot de passe",'class':'form-control', "autofocus": True,'placeholder':'Entrez votre mot de passe'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Nouveau mot de passe confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "Nouveau mot de passe",'class':'form-control','placeholder':'Confirmation du mot de passe'}),
    )
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm,self).__init__(*args,user, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # Méthode du formulaire (post par défaut)
        self.helper.form_class = 'my-login-form'  # Classe CSS pour le formulaire
        self.helper.form_show_labels = True  # Afficher les étiquettes des champs
        self.helper.form_show_errors =True
        self.helper._help_text_inline = True
        self.helper.layout = Layout(
        
            Field('new_password1',css_class='col-md-9'),
            Field('new_password2',css_class='col-md-9'),
            Submit('submit',"Réinitialiser mon mot de passse", css_class='btn btn-primary')
            
        )
