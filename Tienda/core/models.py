from django.db import models

class RolUser(models.Model):
    rol_id = models.AutoField(primary_key=True, verbose_name='ID Rol',)
    rol_nombre = models.CharField(max_length=50, verbose_name='Nombre Rol')

    def str(self):
        return self.rol_nombre

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID Usuario',)
    email = models.EmailField(max_length=50, verbose_name='Correo Electrónico', unique=True)
    nombre_usuario = models.CharField(max_length=100, verbose_name='Nombre de Usuario', unique=True)
    contrasena = models.CharField(max_length=100, verbose_name='Contraseña')
    rol_id = models.ForeignKey(RolUser, on_delete=models.SET_NULL, null=True, related_name='usuarios')

    def str(self):
        return self.nombre_usuario
    
class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True, verbose_name='ID Categoria',)
    categoria_nombre = models.CharField(max_length=100)
    categoria_slug = models.CharField(max_length=100)
    
    def str(self):
        return self.categoria_nombre

class Juego(models.Model):
    juego_id = models.AutoField(primary_key=True, verbose_name='ID Juego',)
    juego_nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='juegos/')
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def str(self):
        return self.juego_nombre