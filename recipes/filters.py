from django_filters import rest_framework as filters, DateFromToRangeFilter
from .models import Recipe, Product


class RecipeFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Recipe
        fields = ['title']


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Product
        fields = ['title']
