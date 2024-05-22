from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPaginations
from .filters import RecipesFilter, IngridientFilter
from .mixins import ModelMixinSet, TagsIngredientMixin
from .serializers import (IngredientsSerializer, TagsSerializer,
                          SubscribeSerializer, RecipesListSerializer,
                          RecipesWritewSerializer, FavoritesSerializer,
                          CartSerializer,)
from recipes.models import (Ingredients, Tags,
                            Subscriptions, Recipes,
                            Favorites, Cart,
                            IngredientsRecipes)
from django.db.models import Sum
from .utils import cart_list
from django.http import HttpResponse


class IngredientViewSet(TagsIngredientMixin):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngridientFilter


class TagsViewSet(TagsIngredientMixin):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all().order_by('-id')
    pagination_class = CustomPaginations
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesListSerializer
        return RecipesWritewSerializer

    @action(
        ["get"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        data = IngredientsRecipes.objects.filter(
            recipes__recipes_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount',))
        pdf = cart_list(data)
        return HttpResponse(
            bytes(pdf.output()),
            content_type='application/pdf')


class FavoritesViewSet(ModelMixinSet):
    serializer_class = FavoritesSerializer
    queryset = Favorites.objects.all()
    lookup_field = 'recipes'


class CartViewSet(ModelMixinSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_field = 'recipes'


class SubscribeViewSet(ModelMixinSet):
    serializer_class = SubscribeSerializer
    queryset = Subscriptions.objects.all()
    lookup_field = 'subscribing'
