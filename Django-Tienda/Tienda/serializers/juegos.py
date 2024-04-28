from rest_framework import serializers
from core.models import Juego

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = '__all__'
