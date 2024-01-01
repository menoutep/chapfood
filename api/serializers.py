from rest_framework import serializers
from accounts.models import CustomUser
from livreurs.models import DossierLivreur, Livraison, Livreur
from base.models import Meal, Category,CartItem,CartItemMeal,Order,PromoCode
def validate_preparation_time(value):
        if value < 0:
            raise serializers.ValidationError("Le temps de préparation doit être un nombre positif.")
        return value
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','password','phone_number']  # Ajoutez d'autres champs au besoin
class CustomUserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']  # Ajoutez d'autres champs au besoin

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000,required=False)
    image = serializers.ImageField( required=False)
    class Meta:
        model = Category
        fields = ['id','name', 'description','image']
class MealSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    # Champ personnalisé pour le nom du repas avec une validation de longueur minimale
    name = serializers.CharField(max_length=100, min_length=3)

    # Champ personnalisé pour la description avec une validation de longueur maximale
    description = serializers.CharField(max_length=1000, required=False)

    # Champ personnalisé pour le temps de préparation avec une validation personnalisée
    preparation_time = serializers.IntegerField(validators=[validate_preparation_time])

    # Champ personnalisé pour le prix avec une validation de montant minimum
    price = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=0.01)
    image = serializers.ImageField()

    class Meta:
        model = Meal
        fields = ['id','category','name', 'description', 'price','image','preparation_time']

    def create(self, validated_data):
         
         meal = Meal.objects.create(**validated_data)
         return meal



class CartItemMealSerializer(serializers.ModelSerializer):
    meal = MealSerializer(read_only=True)
    class Meta:
        model = CartItemMeal
        fields = ['id','cart_item','meal','quantity']

class CartItemSerializer(serializers.ModelSerializer):
    meals = CartItemMealSerializer(read_only=True,many=True,)
    user= CustomUserSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id','user','meals','total']


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'description', 'discount_type']


class OrderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Utilisez le sérialiseur CustomUserSerializer pour le champ 'user'
    items = CartItemMealSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'order_total', 'delivery_address', 'is_delivery', 'is_piece', 'monnaie', 'time_cook', 'created_at']


class DossierLivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierLivreur
        fields = '__all__'

class LivreurSerializer(serializers.ModelSerializer):
    dossier = DossierLivreurSerializer(read_only=True)
    class Meta:
        model = Livreur
        fields = ['id','dossier','position','activity','livraison_count','status']

class LivraisonSerializer(serializers.ModelSerializer):
    livreur = LivreurSerializer(read_only=True)
    order = OrderSerializer(read_only=True,many=True)
    class Meta:
        model = Livraison
        fields = ['id','order','livreur','status']