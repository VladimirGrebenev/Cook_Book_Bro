from django.core.management.base import BaseCommand

from recipes.models import Product, Recipe


class Command(BaseCommand):
    help = 'Fill the database with products'

    def handle(self, *args, **options):
        # Создание продуктов
        products = [
            {'title': 'вода', },
            {'title': 'соль', },
            {'title': 'сахар', },
            {'title': 'перец', },
            {'title': 'лаваш', },
            {'title': 'мясо свинина', },
            {'title': 'рыба', },
            {'title': 'шоколад', },
            {'title': 'яйцо', },
            {'title': 'мука', },
            {'title': 'мясо говядина', },
            {'title': 'мясо куриное', },
            {'title': 'мясо барана', },
            {'title': 'майонез', },
            {'title': 'кетчуп', },
            {'title': 'горчица', },
        ]
        for product_data in products:
            Product.objects.create(**product_data)