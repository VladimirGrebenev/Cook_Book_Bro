from rest_framework import serializers
from .models import Recipe, Product, RecipeProduct


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер класса Recipe"""

    class Meta:
        model = Recipe
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для класса Product"""

    class Meta:
        model = Product
        fields = '__all__'


class RecipeProductSerializer(serializers.ModelSerializer):
    """Сериалайзер класса RecipeProduct"""

    class Meta:
        model = RecipeProduct
        fields = '__all__'
