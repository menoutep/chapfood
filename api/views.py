from django.shortcuts import render
from django.http import JsonResponse
from base.models import Meal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict

@api_view
def api_view(request):
    query = Meal.objects.all().order_by('?').first

    if query:
        data = model_to_dict(query)

    return Response(data)