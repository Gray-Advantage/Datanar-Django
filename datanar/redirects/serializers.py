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


class RedirectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Redirect
        fields = (
            models.Redirect.long_link.field.name,
            models.Redirect.short_link.field.name,
        )


__all__ = [RedirectSerializer, RedirectCreateSerializer]
