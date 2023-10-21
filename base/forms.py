from django import forms
from .models import Meal, Category
from django.utils import timezone
from django.core.validators import RegexValidator
class MealForm(forms.ModelForm):
    # Champ "category" avec liste déroulante (select) de catégories disponibles
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Meal
        fields = ['name', 'description', 'price','image','preparation_time']  # Ajout du champ 'image'

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})

        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control'})
        self.fields['price'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['image'].widget = forms.FileInput(attrs={'class': 'form-control'})
        self.fields['preparation_time'].widget = forms.NumberInput(attrs={'class': 'form-control'})







class DeliveryForm(forms.Form):
    delivery_address = forms.CharField(
        max_length=255,
        required=False,
        label="Adresse de livraison",
        widget=forms.TextInput(attrs={'class': 'form-control rounded'})
    )
    is_piece = forms.BooleanField(
        required=False,
        label="vous avez la monnaie",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    monnaie = forms.DecimalField(
        max_digits=15,  # Le même nombre de chiffres que dans le modèle
        decimal_places=2,  # Le même nombre de décimales que dans le modèle
        required=False,  # Permet de le laisser vide
        label='Monnaie',  # Le label que vous souhaitez afficher
    )
    is_delivery = forms.BooleanField(
        required=False,
        label="Je veux être livré",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pickup_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control rounded', 'type': 'time'}),
        label="indiquer l'heure a laquelle vous voulez prendre le repas"
    )
    def clean(self):
            cleaned_data = super().clean()
            pickup_time = cleaned_data.get('pickup_time')

            if pickup_time is not None:
                current_time = timezone.now().time()

                if pickup_time < current_time:
                    self.add_error('pickup_time', "L'heure de prise de repas ne peut pas être antérieure à l'heure actuelle.")


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',  # Modifiez cette regex en fonction de vos besoins
    message="Le numéro de téléphone doit être au format: '+999999999'. Il peut contenir jusqu'à 15 chiffres."
)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name','id':"name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email','id':'email'}))
    phone = forms.CharField(max_length=20, validators=[phone_regex], widget=forms.TextInput(attrs={'placeholder': 'Phone', 'id': 'phone'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Sujet','id':'subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message','id':'message', 'cols':'30', 'rows':'10'}))
   