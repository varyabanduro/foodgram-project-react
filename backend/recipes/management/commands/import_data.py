from csv import DictReader

from django.core.management.base import BaseCommand

from foodgram_backend.settings import BASE_DIR
from recipes.models import Ingredients


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def ImportIngredients(self):
        if Ingredients.objects.exists():
            print('Данные для User уже загружены')
        else:
            for ingredient in DictReader(open(
                    BASE_DIR / 'static/data/ingredients.csv',
                    encoding='utf8')):
                Ingredients.objects.create(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit'],
                )
            print('Данные для Ingredients загружены')

    def handle(self, *args, **kwargs):
        self.ImportIngredients()
