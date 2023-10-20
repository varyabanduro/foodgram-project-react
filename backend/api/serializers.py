import base64
from rest_framework import serializers
from recipes.models import (Ingredients, Tags,
                            Subscriptions, Recipes,
                            IngredientsRecipes, RecipesTags,
                            Favorites, Cart)
import webcolors
from users.serializers import (SubscriptionsUserSerializer,
                               CustomUserSerializer,
                               SubscriptionsRecipesSerializer)
from django.core.files.base import ContentFile
from .validators import unique_constraint, check_pk


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = (
            'id', 'name', 'measurement_unit'
        )


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tags
        fields = (
            'id', 'name', 'color', 'slug'
        )


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    subscribing = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_representation(self, instance):
        return SubscriptionsUserSerializer(
            instance.subscribing, context=self.context
        ).data

    def validate(self, attrs):
        unique_constraint(self)
        user_id = self.context.get("request").user.id
        subscribing_id = self.context.get('view').kwargs.get('subscribing')
        if user_id == int(subscribing_id):
            raise serializers.ValidationError(
                {"error": 'Нельзя подписаться на самого себя'}
            )
        return attrs

    class Meta:
        model = Subscriptions
        fields = ('user', 'subscribing')


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientsRecipes
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class RecipesListSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = IngredientsRecipesSerializer(
        many=True, source='ingredient_recipes'
    )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        # if not user.is_authenticated:
        #     return False
        # return obj.favorites_recipes.filter(
        #     # user=user, recipes=obj.id
        #     user=user,
        # ).exists()
        return user.is_authenticated and obj.favorites_recipes.filter(
            user=user,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        # if not user.is_authenticated:
        #     return False
        # return obj.recipes_cart.filter(
        #     # user=user, recipes=obj.id
        #     user=user,
        # ).exists()
        return user.is_authenticated and obj.recipes_cart.filter(
            user=user,
        ).exists()

    class Meta:
        model = Recipes
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )


class IngredientsRecipesWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientsRecipes
        fields = (
            'id', 'amount'
        )


class RecipesWritewSerializer(serializers.ModelSerializer):
    ingredients = IngredientsRecipesWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True
    )
    image = Base64ImageField(required=False, allow_null=True)

    def to_representation(self, instance):
        return RecipesListSerializer(
            instance, context=self.context
        ).data

    def _add_ingredients(self, recipe, ingredients):
        lst = []
        for ingredient in ingredients:
            current_ingredient, status = Ingredients.objects.get_or_create(
                id=ingredient.get("id").id
            )
            IngredientsRecipes.objects.create(
                recipes=recipe,
                ingredient=current_ingredient,
                amount=int(ingredient.get("amount"))
            )
            lst.append(current_ingredient)
        return lst

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get("request").user
        recipe = Recipes.objects.create(**validated_data, author=author)
        self._add_ingredients(recipe, ingredients)
        for tag in tags:
            RecipesTags.objects.create(
                tag=tag, recipes=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)

        ingredients_data = validated_data.pop('ingredients')
        IngredientsRecipes.objects.filter(recipes=instance).delete()
        instance.ingredients.set(
            self._add_ingredients(instance, ingredients_data)
        )

        tags_data = validated_data.pop('tags')
        RecipesTags.objects.filter(recipes=instance).delete()
        for tag in tags_data:
            RecipesTags.objects.create(
                tag=tag, recipes=instance
            )

        instance.save()
        return instance

    class Meta:
        model = Recipes
        fields = (
            'tags', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )


class FavoritesCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    recipes = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_representation(self, instance):
        return SubscriptionsRecipesSerializer(
            instance.recipes, context=self.context
        ).data

    def validate(self, attrs):
        unique_constraint(self)
        check_pk(self)
        return attrs


class FavoritesSerializer(FavoritesCartSerializer):
    class Meta:
        model = Favorites
        fields = (
            'user', 'recipes'
        )


class CartSerializer(FavoritesCartSerializer):
    class Meta:
        model = Cart
        fields = (
            'user', 'recipes'
        )
