from rest_framework import serializers


def unique_constraint(self):
    user = self.context.get('request').user
    kwargs = self.context.get('view').kwargs
    model = self.Meta.model
    obj = model.objects.filter(user=user, **kwargs)
    if obj:
        raise serializers.ValidationError(
            {"error": 'Запись уже существует'}
        )


def check_pk(self):
    kwargs = self.context.get('view').kwargs
    lookup_field = self.context.get('view').lookup_field
    pk = kwargs.get(lookup_field)
    try:
        pk = int(pk)
    except ValueError:
        raise serializers.ValidationError(
            {"error": 'id должно быть числом'}
        )
