from django.urls import path
from rest_framework import routers
from .views import (
    RecipeListCreateView,
    RecipeRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    RecipeViewSet,
    ProductViewSet,
    RecipeProductViewSet,
)

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'recipe_products', RecipeProductViewSet,
                basename='recipe_products')

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(),
         name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view(),
         name='recipe-retrieve-update-destroy'),
    path('products/', ProductListCreateView.as_view(),
         name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(),
         name='product-retrieve-update-destroy'),
]

urlpatterns += router.urls
