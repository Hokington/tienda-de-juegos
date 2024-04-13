import json
from django.shortcuts import render, get_object_or_404
from core.models import Juego, Categoria

def index(request):
    juegos = Juego.objects.all()
    context = {'juegos': juegos}
    return render(request, 'index.html', context)

def categoria(request, categoria_slug):
    categoria = get_object_or_404(Categoria, categoria_slug=categoria_slug)

    juegos = Juego.objects.filter(categoria_id=categoria)
    context = {'juegos': juegos,
               'categoria': categoria }
    return render(request, 'categoria.html', context)

def juego(request, juego_id):
    juego = get_object_or_404(Juego, juego_id=juego_id)
    context = {'juego': juego }

    return render(request, 'juego.html', context)