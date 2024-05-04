from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import Categoria, Juego
from .serializers import categorias, juegos
# Create your views here.
@csrf_exempt
@api_view(['GET'])
def lista_categorias(request):
    if request.method == 'GET':
        categoriasObjects = Categoria.objects.all()
        serializer = categorias.CategoriaSerializer(categoriasObjects, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def lista_juegos(request):
    if request.method == 'GET':
        juegosObjects = Juego.objects.all()
        serializer = juegos.JuegoSerializer(juegosObjects, many=True)
        return Response(serializer.data)