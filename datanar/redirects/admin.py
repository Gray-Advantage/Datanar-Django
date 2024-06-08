from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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
    )


@admin.register(redirects_models.Redirect)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "view_long_link",
        redirects_models.Redirect.short_link.field.name,
        redirects_models.Redirect.created_at.field.name,
    )

    @admin.display(
        description=_("long_link"),
    )
    def view_long_link(self, obj):
        if obj.long_link and len(obj.long_link) > 75:
            return obj.long_link[:75] + "..."
        return obj.long_link

    inlines = [
        ClickInline,
    ]


__all__ = []
