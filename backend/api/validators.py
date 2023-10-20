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
    pk = self.kwargs.get(self.lookup_field)
    try:
        pk = int(pk)
    except ValueError:
        raise serializers.ValidationError(
            {"error": 'id должно быть числом'}
        )
