from django.contrib import admin

from core.models import User, RolUser, Categoria, Juego

admin.site.register(User)
admin.site.register(RolUser)
admin.site.register(Categoria)
admin.site.register(Juego)