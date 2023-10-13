from djoser.serializers import UserSerializer
from users.models import User
from rest_framework import serializers
from recipes.models import Recipes


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return obj.subscribing.filter(
                user=request.user,
                subscribing=obj.id
            ).exists()
        return False


class CustomListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
                return data[:recipes_limit]
            except ValueError:
                return data
        return data


class SubscriptionsRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
        list_serializer_class = CustomListSerializer


class SubscriptionsUserSerializer(CustomUserSerializer):
    recipes = SubscriptionsRecipesSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()
