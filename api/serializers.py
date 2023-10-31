from rest_framework import serializers
from base.models import Meal, Category
def validate_preparation_time(value):
        if value < 0:
            raise serializers.ValidationError("Le temps de préparation doit être un nombre positif.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000,required=False)
    image = serializers.ImageField( required=False)
    class Meta:
        model = Category
        fields = ('name', 'description','image')
class MealSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)

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
        fields = ('category','name', 'description', 'price','image','preparation_time')

    def create(self, validated_data):
         
         meal = Meal.objects.create(**validated_data)
         return meal


