from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Tags(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[\w\s]+\Z',
                message='Тег состоит только из букв',
            ),
        ),
        verbose_name='Тэг',
        help_text='Название тега'
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Цвет',
        help_text='Цвет тега'
    )
    slug = models.SlugField(
        max_length=32,
    )

    class Meta:
        verbose_name = 'Тэги'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.name


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    subscribing = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscribing"],
                name="unique_subscribe",
            ),
        ]


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Ингридиент',
        help_text='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингридиенты'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self) -> str:
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=200,
        validators=(
            RegexValidator(
                regex=r'^[\w\s,]+\Z',
                message='Название рецепта состоит только из букв',
            ),
        ),
        verbose_name='Название',
        help_text='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Описание',
        help_text='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=(
            MinValueValidator(1),
        ),
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipesTags',
        blank=False,
        verbose_name='Тэг'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsRecipes',
        blank=True,
        verbose_name='Ингридиент'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользоваетль'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorites_recipes',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipes"],
                name="unique_favorites",
            ),
        ]


class IngredientsRecipes(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингридиенты'
    )
    # Как я поняла у нас это в тз, но в ингридиетах
    # есть "по вкусу" и мне кажется было бы круто сделать,
    # что бы в таких ингридиетах была возможность оставлять поле пустым
    # а так у нас получается авокадо-1(по вкусу)
    amount = models.PositiveSmallIntegerField(
        blank=False,
        validators=(
            MinValueValidator(1),
        ),
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингридиетны'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class RecipesTags(models.Model):
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name='Теги'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "recipes"],
                name="unique_tag-recipes",
            ),
        ]

    def __str__(self):
        return f'{self.tag} {self.recipes}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipes_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipes"],
                name="unique_cart",
            ),
        ]
