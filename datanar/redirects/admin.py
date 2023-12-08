from django.contrib import admin

from redirects import models as redirects_models
from statistic import models as statistic_models


class ClickInline(admin.TabularInline):
    model = statistic_models.Click
    extra = 0

    readonly_fields = (
        statistic_models.Click.id.field.name,
        statistic_models.Click.country.field.name,
        statistic_models.Click.city.field.name,
        statistic_models.Click.os.field.name,
        statistic_models.Click.browser.field.name,
        statistic_models.Click.referrer.field.name,
    )


@admin.register(redirects_models.Redirect)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        redirects_models.Redirect.long_link.field.name,
        redirects_models.Redirect.short_link.field.name,
    )

    inlines = [
        ClickInline,
    ]


__all__ = []
