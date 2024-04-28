import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from core.models import Juego, Categoria, User, RolUser
from core.forms import RegistroForm, LoginForm, EditProfileForm, JuegoForm
from django.contrib import messages
from rest_framework import generics
from .serializers import categorias, juegos

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

# AUTH #

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            rol = RolUser.objects.get(rol_id=1)
            user = User(
                nombre = form.cleaned_data['nombre'],
                nombre_usuario = form.cleaned_data['nombre_usuario'],
                email=form.cleaned_data['email'],
                direccion = form.cleaned_data['direccion'],
                fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
                contrasena = form.cleaned_data['password1'],
                rol_id = rol,
            )

            user.save()

            return redirect("login")
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = User.objects.get(email = email)
            request.session['username'] = user.nombre_usuario
            request.session['user_id'] = user.id
            request.session['rol_id'] = user.rol_id.pk

            if user.rol_id.pk == 1:
                return redirect('mi-perfil')
            if user.rol_id.pk == 2:
                return redirect('admin-panel')
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    request.session.clear()
    return redirect('index')


def role_required(required_role_id):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            rol_id = request.session.get('rol_id')
            if not rol_id or rol_id != required_role_id:
                return redirect('index')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def mi_perfil(request):
    user_id = request.session.get('user_id')
    rol_id = request.session.get('rol_id')
    if not rol_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('mi-perfil')
    else:
        form = EditProfileForm(instance=user)
        
    return render(request, 'mi-perfil.html', {"form": form})

@role_required(2)
def admin_panel(request):
    rol_id = request.session.get('rol_id')
    if not rol_id or not rol_id == 2:
        return redirect('index')
    
    juegos = Juego.objects.all()
    context = {
        'juegos': juegos
    }
    return render(request, 'admin-panel.html', context)

@role_required(2)
def juego_create(request):
    if request.method == 'POST':
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El Juego ha sido creado con éxito.')
            return redirect('admin-panel')
        else:
            messages.error(request, 'Hubo un error al crear el juego. Por favor, verifica el formulario.')
    else:
        form = JuegoForm()

    return render(request, 'juego-create.html', {'form': form})

@role_required(2)
def juego_update(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    if request.method == 'POST':
        form = JuegoForm(request.POST, instance=juego)
        if form.is_valid():
            form.save()
            messages.success(request, 'El juego ha sido actualizado con éxito.')
            return redirect('admin-panel')
    else:
        form = JuegoForm(instance=juego)
        
    context = {
        "form": form,
        "juego": juego
    }
    return render(request, 'juego-update.html', context)

@role_required(2)
def juego_delete(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    if request.method == 'POST':
        juego.delete()
        messages.success(request, 'El juego ha sido eliminado con éxito.')
        return redirect('admin-panel')

    return redirect('admin-panel')

class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = categorias.CategoriaSerializer

class CategoriaDetailView(generics.RetrieveAPIView):
    queryset = Categoria.objects.all()
    serializer_class = categorias.CategoriaSerializer

class JuegoListView(generics.ListAPIView):
    queryset = Juego.objects.all()
    serializer_class = juegos.CategoriaSerializer

class JuegoDetailView(generics.RetrieveAPIView):
    queryset = Juego.objects.all()
    serializer_class = juegos.CategoriaSerializer

def mmo_api(request):

    response = requests.get('https://www.mmobomb.com/api1/games?sort-by=relevance')
    if response.status_code == 200:
        datos_api = response.json()

    context = {
        "juegos": datos_api
    }
        
    return render(request, 'mmo.html', context)

def ofertas_api(request):

    response = requests.get('https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15')
    if response.status_code == 200:
        datos_api = response.json()

    context = {
        "juegos": datos_api
    }
        
    return render(request, 'ofertas.html', context)
