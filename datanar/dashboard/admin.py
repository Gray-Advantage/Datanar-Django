from django.contrib import admin

from dashboard.models import BlockedDomain


@admin.register(BlockedDomain)
class ItemAdmin(admin.ModelAdmin):
    list_display = (BlockedDomain.domain_regex.field.name,)


__all__ = []
