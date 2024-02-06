from django.db import models
from users.models import CustomUser
from uuid import uuid4

class Product(models.Model):
    """Продукт входящий в рецепт"""
    title = models.CharField(verbose_name='recipe_title', max_length=250,
                             unique=True)
    cooked_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class Recipe(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, verbose_name='id')
    """Рецепт с формулой состоящей из продуктов и граммов"""
    title = models.CharField(verbose_name='recipe_title',
                             max_length=250, unique=True)
    products = models.ManyToManyField(Product, through='RecipeProduct')

    def __str__(self):
        return f'{self.title}'


class RecipeProduct(models.Model):
    """Продукты, входящие в рецепт с указанием веса"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.recipe.title} - {self.product.title}'
