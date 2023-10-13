from djoser.views import UserViewSet
from api.pagination import CustomPaginations
from rest_framework.decorators import action
from .serializers import SubscriptionsUserSerializer
from rest_framework import response, permissions
from .models import User
from rest_framework.permissions import IsAuthenticated


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPaginations

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(
        ["get"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=SubscriptionsUserSerializer
    )
    def subscriptions(self, request, *args, **kwargs):
        sub = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(sub)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(sub, many=True)
        return response.Response(serializer.data)
