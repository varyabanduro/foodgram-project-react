from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (IngredientViewSet, TagsViewSet,
                    SubscribeViewSet, RecipesViewSet,
                    FavoritesViewSet, CartViewSet)
from users.views import CustomUserViewSet
from .routers import FavoritesRouter

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipesViewSet, basename='recipes')

subscribe_router = FavoritesRouter()
subscribe_router.register('subscribe', SubscribeViewSet, basename='subscribe')

recipes_router = FavoritesRouter()
recipes_router.register('favorite', FavoritesViewSet)
recipes_router.register('shopping_cart', CartViewSet)

auth_patterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/', include(recipes_router.urls)),
    path('users/', include(subscribe_router.urls)),
    path('', include(auth_patterns)),
]
