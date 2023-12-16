from rest_framework import serializers

from redirects import models


class RedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Redirect
        fields = (
            models.Redirect.id.field.name,
            models.Redirect.long_link.field.name,
            models.Redirect.short_link.field.name,
            models.Redirect.created_at.field.name,
            models.Redirect.password.field.name,
            models.Redirect.validity_clicks.field.name,
        )


class RedirectCreateSerializer(serializers.Serializer):
    short_link = serializers.CharField(max_length=50, required=False)
    long_link = serializers.URLField(max_length=2000, required=True)
    password = serializers.CharField(max_length=128, required=False)
    validity_days = serializers.IntegerField(default=90, required=False)
    validity_clicks = serializers.IntegerField(default=None, required=False)

    def create(self, validated_data):
        return models.Redirect.objects.create(**validated_data)


__all__ = [RedirectSerializer, RedirectCreateSerializer]
