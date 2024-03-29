from rest_framework import viewsets, generics, mixins
from django.shortcuts import get_object_or_404
from recipes.models import Recipes
from users.models import User


class TagsIngredientMixin(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class ModelMixinSet(generics.CreateAPIView,
                    generics.DestroyAPIView,
                    viewsets.GenericViewSet):

    def get_model(self):
        if self.lookup_field in ('recipes',):
            return Recipes
        return User

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user = self.request.user
        return get_object_or_404(queryset, user=user, **self.kwargs)

    def perform_create(self, serializer):
        pk = self.kwargs.get(self.lookup_field)
        attr = {
            self.lookup_field: get_object_or_404(self.get_model(), pk=pk)
        }
        serializer.save(user=self.request.user, **attr)
