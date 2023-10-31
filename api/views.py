from django.shortcuts import render
from django.http import JsonResponse
import json
from base.models import Meal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from api.serializers import MealSerializer,CategorySerializer
from rest_framework import generics
@api_view(["POST"])
def index(request):
    print(request.data)
    
    instance = CategorySerializer(data=request.data)
    if instance.is_valid(raise_exception=True):
        instance.save()
        #instance.save()
        return Response(instance.data)
    
class DetailApiView(generics.RetrieveAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class CreateApiView(generics.CreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


   