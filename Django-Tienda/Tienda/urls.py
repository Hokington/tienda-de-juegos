"""
URL configuration for Tienda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('categoria/<str:categoria_slug>', views.categoria, name='categoria'),
    path('juego/<int:juego_id>', views.juego, name="juego"),

    path('mi-perfil/', views.mi_perfil, name='mi-perfil'),
    path('admin-panel/', views.admin_panel, name='admin-panel'),
    path('admin-panel/juegos/nuevo/', views.juego_create, name='juego_create'),
    path('admin-panel/juegos/<int:pk>/editar', views.juego_update, name='juego_update' ),
    path('admin-panel/juegos/<int:pk>/borrar', views.juego_delete, name='juego_delete' ),

    path('api/categorias/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('api/categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),
    
    path('api/juegos/', views.JuegoListView.as_view(), name='categoria-list'),
    path('api/juegos/<int:pk>/', views.JuegoDetailView.as_view(), name='categoria-detail'),

    path('mmo/', views.mmo_api, name='mmo'),
    path('ofertas/', views.ofertas_api, name='ofertas'),
]
