from django_filters.rest_framework import (CharFilter, FilterSet,
                                           NumberFilter, BooleanFilter,
                                           ModelMultipleChoiceFilter)
from recipes.models import Recipes, Ingredients, Tags


class RecipesFilter(FilterSet):
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')
    author = NumberFilter(field_name='author')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all()
    )

    class Meta:
        model = Recipes
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites_recipes__user=self.request.user)
        return queryset.all()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(recipes_cart__user=self.request.user)
        return queryset.all()


class IngridientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ('name',)
