from django.core.management.base import BaseCommand

from users.models import CustomUser, UserRoles


class Command(BaseCommand):
    help = 'Fill the database with users'

    def handle(self, *args, **options):
        # добавляем тестовых пользователей
        CustomUser.objects.filter(email__startswith='test').delete()
        for i in range(3):
            CustomUser.objects.create_user(
                first_name=f'first name {i}',
                last_name=f'last name {i}',
                user_name=f'user{i}',
                email=f'test_mail{i}@mail.ru',
                password=f'pass{i}'
            )

        # добавляем тестовых поваров
        for i in range(3):
            CustomUser.objects.create_user(
                first_name=f'cook name {i}',
                last_name=f'cook name {i}',
                user_name=f'cook{i}',
                email=f'test_cook{i}@mail.ru',
                password=f'pass{i}',
                role=UserRoles.COOK
            )

        # добавляем тестового шеф-повара
        CustomUser.objects.filter(email__startswith='chef').delete()
        chef = CustomUser(
            email='chef@mail.ru',
            first_name='chef_name',
            last_name='chef_surname',
            user_name='chef_name',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role=UserRoles.CHEF
        )
        chef.set_password('123')
        chef.save()

        # добавляем тестового админа superuser
        CustomUser.objects.filter(email='admin@mail.ru').delete()
        CustomUser.objects.create_superuser('admin@mail.ru', 'admin',
                                            user_name='admin',
                                            role=UserRoles.CHEF)
