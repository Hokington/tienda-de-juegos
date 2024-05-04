from django.urls import path
from rest_api.views import lista_categorias, lista_juegos

urlpatterns = [
    path('lista_categorias/', lista_categorias, name="lista_categorias"),
    path('lista_juegos/', lista_juegos, name="lista_juegos")
]