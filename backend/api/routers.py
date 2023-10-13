from rest_framework.routers import Route, DefaultRouter


class FavoritesRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{lookup}/{prefix}/$',
            mapping={
                'get': 'retrieve',
                'post': 'create',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Create'}
        ),
    ]
