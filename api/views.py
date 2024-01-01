from django.shortcuts import render
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login
from base.views import customer_required
from rest_framework.authtoken.models import Token
from base.models import Meal,CartItem,PromoCode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from accounts.models import CustomUser
from api.serializers import MealSerializer,CategorySerializer,CustomUserLoginSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer

class CustomUserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]

        # Vérification si le nom d'utilisateur existe déjà
            if CustomUser.objects.filter(username=username).exists():
                return Response(data={"error": "Ce nom d'utilisateur existe déjà."}, status=400)

            # Vérification si l'email existe déjà
            if CustomUser.objects.filter(email=email).exists():
                return Response(data={"error": "Cet email existe déjà."}, status=400)
                # Création d'un nouvel utilisateur

            user = serializer.save()

            # Tu peux ajouter d'autres actions ici, comme l'envoi de courriels de confirmation, etc.

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

@api_view(["POST","GET"])
def login(request):
    response_data = {}
    if request.method == "POST":
        data = request.data
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None : 
                login(request, user)
                token=Token.objects.get(user=user)
                if token is not None: 
                    response_data = {"token":token}

                

    return Response(response_data)
@api_view(["GET"])
def index(request):
    response_data = {"ok":"ok"}
    for user in CustomUser.objects.all():
        token=Token.objects.get_or_create(user=user) 
        
    return Response(response_data)
    
class DetailApiView(generics.RetrieveAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class CreateApiView(generics.CreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


@customer_required
@api_view(["POST","GET"])
def cart(request):
    response_data = {}
    if request.method == 'GET':
        customer = CustomUser.objects.get(username=request.user.username,email=request.user.email)
        cart, created = CartItem.objects.get_or_create(user=customer,last=True)
        total = cart.calculate_total()
        code_promo= request.GET.get('code_promo')
        ancien_total = 0
        if code_promo:
            ancien_total = total
            if isinstance(code_promo, str):
                promo = PromoCode.objects.get(code=code_promo)
                promo.is_active()
                print(promo.active)
                if promo and promo.active:
                    print(promo.discount_type)
                    if promo.discount_type=='percent':
                        discount = (total * promo.discount_value)/100
                        cart.total = total-discount
                        cart.save()
                        promo.active = False
                        promo.save()
                    elif promo.discount_type == 'amount':
                        discount = promo.discount_value
                        cart.total = total - discount
                        cart.save()
                        promo.active = False
                        promo.save()

    response_data = {'cart': cart, 'total': cart.total,'ancien_total':ancien_total}   

    return Response(response_data)
   