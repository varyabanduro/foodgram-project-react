# Generated by Django 3.2.3 on 2023-10-03 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsrecipes',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingrredient_recipes', to='recipes.recipes', verbose_name='Рецепт'),
        ),
    ]