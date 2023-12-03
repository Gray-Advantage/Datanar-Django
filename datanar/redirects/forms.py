from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import sqids

from redirects.models import Redirect


class RedirectForm(forms.ModelForm):
    custom_url = forms.CharField(
        label=_("custom_url"),
        help_text=_("custom_url_that_would_like_have_instead_generated_one"),
        max_length=50,
        required=False,
    )

    class Meta:
        model = Redirect

        fields = [
            Redirect.long_link.field.name,
        ]

        exclude = [
            Redirect.user.field.name,
            Redirect.short_link.field.name,
            Redirect.created_at.field.name,
            Redirect.password.field.name,
            Redirect.validity_days.field.name,
            Redirect.validity_clicks.field.name,
        ]

    def clean_custom_url(self):
        custom_url = self.cleaned_data.get("custom_url")

        if custom_url and Redirect.objects.get_by_short_link(custom_url):
            raise ValidationError(_("custom_url_already_use"))

        short_link = sqids.generate()
        while Redirect.objects.get_by_short_link(short_link):
            short_link = sqids.generate()

        self.cleaned_data["short_link"] = short_link
        return custom_url


__all__ = [RedirectForm]
