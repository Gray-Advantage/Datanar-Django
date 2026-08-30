from urllib.parse import urlparse

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dashboard.models import BlockedDomain
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
            return f"{obj.long_link[:75]}..."
        return obj.long_link

    @admin.action(description=_("block_selected_redirects"))
    def block(self, request, queryset):
        regex_urls = set()

        for url in queryset.values_list("long_link", flat=True):
            netloc = urlparse(url).netloc.split(":")[0]
            parts = netloc.split(".")
            if len(parts) >= 2:
                main_domain = parts[-2]
                regex_urls.add(f"||{main_domain}^")
            elif parts[0]:
                regex_urls.add(f"||{parts[0]}^")

        blocked_domains = [
            BlockedDomain(domain_regex=regex) for regex in regex_urls
        ]
        BlockedDomain.objects.bulk_create(
            blocked_domains,
            ignore_conflicts=True,
        )

        queryset.delete()

        self.message_user(request, _("success_block_selected_redirect"))

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
    actions = ["block", "deactivate", "activate"]


__all__ = []
