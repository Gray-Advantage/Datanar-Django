from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.forms import BootstrapFormMixin
from core.widgets import DatePickerInput
from dashboard.models import BlockedDomain
from redirects.models import Redirect
from redirects.utils import generate_short_link


class RedirectForm(BootstrapFormMixin, forms.ModelForm):
    custom_url = forms.SlugField(
        label=_("custom_url"),
        help_text=_("custom_url_that_would_like_have_instead_generated_one"),
        max_length=50,
        allow_unicode=True,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i, field in enumerate(self.fields.values()):
            if field.help_text:
                field.widget.attrs["placeholder"] = field.help_text
            if i > 0:
                field.widget.attrs["class"] += " mb-2"

    class Meta:
        model = Redirect

        fields = [
            Redirect.long_link.field.name,
        ]

    def clean(self):
        if self.errors:
            return super().clean()

        long_link = self.cleaned_data.get(Redirect.long_link.field.name)
        custom_url = self.cleaned_data.get("custom_url")

        if custom_url:
            if "/" in custom_url:
                self.add_error(
                    "custom_url",
                    ValidationError(_("custom_url_should_not_have_slash")),
                )
            if Redirect.objects.get_by_short_link(custom_url):
                self.add_error(
                    "custom_url",
                    ValidationError(_("custom_url_already_use")),
                )

            if BlockedDomain.objects.is_blocked(long_link):
                self.add_error(
                    Redirect.long_link.field.name,
                    ValidationError(_("this_url_is_blocked")),
                )

            if not self.errors:
                self.cleaned_data[Redirect.short_link.field.name] = custom_url
                del self.cleaned_data["custom_url"]
                return self.cleaned_data

            return None

        if BlockedDomain.objects.is_blocked(long_link):
            self.add_error(
                Redirect.long_link.field.name,
                ValidationError(_("this_url_is_blocked")),
            )
            return None
        self.cleaned_data[Redirect.short_link.field.name] = generate_short_link(
            self.cleaned_data[Redirect.long_link.field.name],
        )
        del self.cleaned_data["custom_url"]

        return self.cleaned_data


class RedirectFormExtended(RedirectForm):
    links_file = forms.FileField(required=False)

    date_validity_field = forms.DateField(
        label=Redirect.validity_days.field.verbose_name.capitalize(),
        help_text=Redirect.validity_days.field.help_text,
        widget=DatePickerInput(),
        required=False,
    )

    field_order = [
        Redirect.long_link.field.name,
        "custom_url",
        Redirect.password.field.name,
        "date_validity_field",
        Redirect.validity_clicks.field.name,
        "links_file",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["links_file"].widget.attrs["class"] = "d-none"
        self.fields["links_file"].widget.attrs["accept"] = ".txt, .xlsx"

    def clean(self):
        if self.errors:
            return super().clean()

        if self.cleaned_data["date_validity_field"] is None:
            self.cleaned_data[Redirect.validity_days.field.name] = None
            del self.cleaned_data["date_validity_field"]
            return super().clean()

        delta = (
            self.cleaned_data["date_validity_field"] - timezone.now().date()
        )

        if delta.days < 0:
            self.add_error("date_validity_field", _("date_validity_invalid"))
        else:
            self.cleaned_data[Redirect.validity_days.field.name] = delta.days
            del self.cleaned_data["date_validity_field"]

        return super().clean()

    class Meta(RedirectForm.Meta):
        fields = [
            Redirect.long_link.field.name,
            "custom_url",
            Redirect.password.field.name,
            "date_validity_field",
            Redirect.validity_clicks.field.name,
        ]


class PasswordForm(BootstrapFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"placeholder": field.help_text})

    password = forms.CharField(
        label=_("Password"),
        help_text=_("password_before_redirect"),
    )


__all__ = ["RedirectForm", "RedirectFormExtended", "PasswordForm"]
