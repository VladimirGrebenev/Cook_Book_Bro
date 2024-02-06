from rest_framework import generics
from .models import Recipe, Product, RecipeProduct
from .serializers import RecipeSerializer, ProductSerializer, \
    RecipeProductSerializer
from rest_framework.pagination import LimitOffsetPagination
from .filters import RecipeFilter, ProductFilter
from .permissions import IsChef, IsCook
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q


# пагинатор для Recipe
class RecipeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 15


# пагинатор для Product
class ProductLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 15


class RecipeListCreateView(generics.ListCreateAPIView):
    """List all Recipes or create new Recipe"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeLimitOffsetPagination
    filterset_class = RecipeFilter


class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """By Recipe pk, you can retrieve, update or patch, delete Recipe"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsChef]
        elif self.request.method in ['PUT', 'PATCH']:
            permission_classes = [IsAuthenticated, IsTeacher | IsChef]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeLimitOffsetPagination
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsChef]
        elif self.request.method in ['PUT', 'PATCH']:
            permission_classes = [IsAuthenticated, IsTeacher | IsChef]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def cook_recipe(self, request, pk=None):
        """ Cook_recipe параметром recipe_id. Функция увеличивает на
        единицу количество приготовленных блюд для каждого продукта,
        входящего в указанный рецепт."""
        recipe = self.get_object()
        recipe_products = RecipeProduct.objects.filter(recipe=recipe)

        for recipe_product in recipe_products:
            product = recipe_product.product
            product.cooked_count += 1
            product.save()

        return Response({'message': 'Recipe cooked successfully'})


class ProductListCreateView(generics.ListCreateAPIView):
    """List all Product or create new Product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductLimitOffsetPagination
    filterset_class = ProductFilter


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """By Product pk, you can retrieve, update or patch, delete
    Product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            permission_classes = [IsAuthenticated, IsChef]
        elif self.request.method in ['GET', 'PUT', 'PATCH']:
            permission_classes = [IsAuthenticated, IsCook | IsChef]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductLimitOffsetPagination
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            permission_classes = [IsAuthenticated, IsChef]
        elif self.request.method in ['GET', 'PUT', 'PATCH']:
            permission_classes = [IsAuthenticated, IsCook | IsChef]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def show_recipes_without_product(self, request):
        """Show_recipes_without_product с параметром title. Функция
        возвращает список. В списке отображены id и названия всех рецептов,
        в которых указанный продукт отсутствует, или присутствует в количестве
        меньше 10 грамм."""

        product_title = request.GET.get('title')

        product = get_object_or_404(Product, title=product_title)
        recipes = Recipe.objects.filter(
            Q(products__isnull=True) | Q(recipeproduct__product=product,
                                         recipeproduct__weight__lt=10)
        ).values('id', 'title')

        return JsonResponse(list(recipes), safe=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверяем, используется ли продукт в рецептах
        if RecipeProduct.objects.filter(product=instance).exists():
            recipes = Recipe.objects.filter(recipeproduct__product=instance)
            recipe_data = [{'id': recipe.id, 'title': recipe.title} for recipe
                           in recipes]
            return Response({
                'message': 'Cannot delete product. It is used in the following recipes:',
                'recipes': recipe_data}, status=400)

        self.perform_destroy(instance)
        return Response(status=204)


class RecipeProductViewSet(viewsets.ModelViewSet):
    queryset = RecipeProduct.objects.all()
    serializer_class = RecipeProductSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            permission_classes = [IsAuthenticated, IsChef]
        elif self.request.method in ['GET', 'PUT', 'PATCH']:
            permission_classes = [IsAuthenticated, IsCook | IsChef]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


