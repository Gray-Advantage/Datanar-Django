from django.contrib import admin
from django.utils import timezone
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
        redirects_models.Redirect.is_active.field.name,
        redirects_models.Redirect.create_method.field.name,
        redirects_models.Redirect.user.field.name,
    )

    @admin.display(description=_("long_link"))
    def view_long_link(self, obj):
        if obj.long_link and len(obj.long_link) > 75:
            return obj.long_link[:75] + "..."
        return obj.long_link

    @admin.action(description=_("deactivate_selected_redirects"))
    def deactivate(self, request, queryset):
        queryset.update(
            is_active=False,
            deactivated_at=timezone.now(),
        )
        self.message_user(request, _("success_deactivate_selected_redirect"))

    @admin.action(description=_("activate_selected_redirects"))
    def activate(self, request, queryset):
        queryset.update(
            is_active=True,
            deactivated_at=None,
            validity_days=None,
        )
        self.message_user(request, _("success_activate_selected_redirect"))

    inlines = [ClickInline]
    actions = ["deactivate", "activate"]


__all__ = []
