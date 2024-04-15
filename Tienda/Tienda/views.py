import json
from django.shortcuts import render, get_object_or_404, redirect
from core.models import Juego, Categoria, User, RolUser
from core.forms import RegistroForm, LoginForm, EditProfileForm
from django.contrib import messages

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

def admin_panel(request):
    rol_id = request.session.get('rol_id')
    if not rol_id or not rol_id == 2:
        return redirect('index')
    
    juegos = Juego.objects.all()

    context = {
        'juegos': juegos
    }
    return render(request, 'admin-panel.html', context)