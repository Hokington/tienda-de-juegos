from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from .models import User, RolUser, Juego, Categoria  # Importa el modelo User y RolUser

class RegistroForm(forms.Form):
    nombre = forms.CharField(label='Nombre Completo', max_length=80, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre_usuario = forms.CharField(label='Nombre de usuario', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo electrónico',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label='Dirección de despacho',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    fecha_nacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=6,
        max_length=18,
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=6,
        max_length=18,
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        birth_date = cleaned_data.get('fecha_nacimiento')

         # Verificar que el email sea único
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('El correo electrónico ya está en uso. Por favor, elija otro.'))
        
        # Verificar que las contraseñas coincidan
        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Las contraseñas deben coincidir'))

        # Verificar que el usuario tenga al menos 13 años
        if birth_date:
            edad = (date.today() - birth_date).days / 365
            if edad < 13:
                raise ValidationError(_('Debes tener al menos 13 años para registrarte'))

        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', max_length=40, widget=forms.EmailInput())
    contrasena = forms.CharField(label='Contraseña', max_length=20, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        contrasena = cleaned_data.get('contrasena')

        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:   
            raise forms.ValidationError('Este usuario no existe.')

        if not usuario.contrasena == contrasena:
            raise forms.ValidationError('Las credenciales no coinciden.')

        return cleaned_data
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nombre_usuario', 'direccion', 'contrasena']
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'contrasena': forms.TextInput(attrs={'class': 'form-control'}),
        }

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['juego_nombre', 'descripcion', 'precio', 'imagen', 'categoria_id']
        widgets = {
            'juego_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(),
            'categoria_id': forms.Select(attrs={'class': 'form-control'}),
        }