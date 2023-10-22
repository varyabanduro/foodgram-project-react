from django.contrib import admin
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown import filters
from recipes.models import (
    Subscriptions,
    Ingredients,
    Favorites,
    Recipes,
    Tags,
    Cart
)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_per_page = 20
    empty_value_diplay = '-пусто-'


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscribing')
    search_fields = ('user',)
    list_per_page = 20
    empty_value_display = '-пусто-'


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = (
        ('name', filters.DropdownFilter),
        ('measurement_unit', filters.DropdownFilter),
    )
    list_per_page = 20
    ordering = ('name',)
    empty_value_diplay = '-пусто-'


@admin.register(Favorites, Cart)
class FavoritesCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipes',)
    list_per_page = 20
    empty_value_diplay = '-пусто-'


class TagsInline(admin.TabularInline):
    model = Recipes.tags.through
    extra = 1


class IngredientsInline(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author',
        'get_html_photo', 'text',
        'cooking_time', 'get_count_favorits'
    )
    list_display_links = ('name', 'author', 'get_html_photo')
    search_fields = ('name',)
    list_filter = (
        ('name', filters.DropdownFilter),
        ('author', filters.RelatedDropdownFilter),
        ('tags', filters.RelatedDropdownFilter),
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
