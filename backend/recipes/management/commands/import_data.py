from csv import DictReader
from django.core.management.base import BaseCommand
from foodgram_backend.settings import BASE_DIR
from recipes.models import Ingredients, Tags, User
import os


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def ImportIngredients(self):
        if Ingredients.objects.exists():
            print('Данные для Ingredients уже загружены')
        else:
            for ingredient in DictReader(open(
                    BASE_DIR / 'static/data/ingredients.csv',
                    encoding='utf8')):
                Ingredients.objects.create(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit'],
                )
            print('Данные для Ingredients загружены')

    def ImportTags(self):
        if Tags.objects.exists():
            print('Данные для Tags уже загружены')
        else:
            for tag in DictReader(open(
                    BASE_DIR / 'static/data/tags.csv',
                    encoding='utf8')):
                Tags.objects.create(
                    name=tag['name'],
                    color=tag['color'],
                    slug=tag['slug']
                )
            print('Данные для Tags загружены')

    def ImportUser(self):
        if User.objects.filter(username='admin').exists():
            print('Данные для User уже загружены')
        else:
            USER_ADMIN_PASSWORD = os.getenv('USER_ADMIN_PASSWORD', 0)
            USER_ADMIN_EMAIL = os.getenv('USER_ADMIN_EMAIL', 0)
            if (USER_ADMIN_EMAIL and USER_ADMIN_PASSWORD):
                result = {
                    'email': USER_ADMIN_EMAIL,
                    'username': 'admin',
                    'first_name': 'admin',
                    'last_name': 'admin',
                    'password': USER_ADMIN_PASSWORD,
                    'is_staff': 1,
                    'is_superuser': 1
                }
                User.objects.create_user(**result)
                print('Admin добавлен')
            else:
                print('Данные Admin не предоставлены')

    def handle(self, *args, **kwargs):
        self.ImportIngredients()
        self.ImportTags()
        self.ImportUser()
