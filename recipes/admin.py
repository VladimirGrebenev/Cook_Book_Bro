from django.contrib import admin
from .models import Recipe, Product, RecipeProduct


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'cooked_count',)
    list_filter = ('title',)
    search_fields = ('title', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Product, ProductAdmin)



# class RecipeProductAdmin(admin.ModelAdmin):
#     list_display = ('recipe', 'product', 'weight')
#     list_filter = ('recipe', 'product')
#     search_fields = ('recipe', 'product')
#
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('title', 'products',)
#     list_filter = ('title',)
#     search_fields = ('title', 'products')