from django.contrib import admin
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from recipes.models import (
    Tags,
    Subscriptions,
    Ingredients,
    Favorites,
    Recipes,
    Cart
    )


class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_per_page = 20
    empty_value_diplay = '-пусто-'


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscribing')
    search_fields = ('user',)
    list_per_page = 20
    empty_value_display = '-пусто-'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = (
        ('name', DropdownFilter),
        ('measurement_unit', DropdownFilter),
    )
    list_per_page = 20
    ordering = ('name',)
    empty_value_diplay = '-пусто-'


class FavoritesCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipes',)
    list_per_page = 20
    empty_value_diplay = '-пусто-'


class TagsInline(admin.TabularInline):
    model = Recipes.tags.through
    extra = 1
    can_delete = False


class IngredientsInline(admin.TabularInline):
    model = Recipes.ingrredients.through
    extra = 1
    can_delete = False


class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author',
        'get_html_photo', 'text',
        'cooking_time', 'get_count_favorits'
    )
    list_display_links = ('name', 'author', 'get_html_photo')
    search_fields = ('name',)
    list_filter = (
        ('name', DropdownFilter),
        ('author', RelatedDropdownFilter),
        ('tags', RelatedDropdownFilter),
    )
    inlines = [
        TagsInline,
        IngredientsInline
    ]
    fields = (
        'get_html_photo', 'image', 'author',
        'name', 'text', 'cooking_time',
        'get_count_favorits'
    )
    list_per_page = 20
    readonly_fields = ('get_html_photo', 'get_count_favorits')
    empty_value_display = '-пусто-'

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=150>")
    get_html_photo.short_description = 'Фото'

    def get_count_favorits(self, object):
        return object.favorites_recipes.count()
    get_count_favorits.short_description = 'В избранном'


admin.site.register(Tags, TagsAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Favorites, FavoritesCartAdmin)
admin.site.register(Cart, FavoritesCartAdmin)
admin.site.register(Recipes, RecipesAdmin)
