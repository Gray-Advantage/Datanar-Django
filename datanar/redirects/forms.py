import hashlib

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from sqids import Sqids

from core.forms import BootstrapFormMixin
from dashboard.models import BlockedDomain
from redirects.models import Redirect


sqids = Sqids()


class CustomDateField(forms.DateInput):
    input_type = "date"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_min_date()

    def update_min_date(self):
        self.attrs["min"] = timezone.localdate()


class RedirectForm(BootstrapFormMixin, forms.ModelForm):
    custom_url = forms.CharField(
        label=_("custom_url"),
        help_text=_("custom_url_that_would_like_have_instead_generated_one"),
        max_length=50,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        first = True
        for field in self.fields.values():
            field.widget.attrs.update({"placeholder": field.help_text})
            if not first:
                field.widget.attrs["class"] += " mb-2"
            first = False

    class Meta:
        model = Redirect

        fields = [
            Redirect.long_link.field.name,
            "custom_url",
        ]

        exclude = [
            Redirect.user.field.name,
            Redirect.short_link.field.name,
            Redirect.created_at.field.name,
            Redirect.password.field.name,
            Redirect.validity_days.field.name,
            Redirect.validity_clicks.field.name,
            Redirect.is_active.field.name,
            Redirect.deactivated_at.field.name,
            Redirect.ip_address.field.name,
            Redirect.create_method.field.name,
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

        counter = 0
        string = self.cleaned_data[Redirect.long_link.field.name]
        while True:
            temp_string = f"{string}{counter}" if counter > 0 else string
            hash_object = hashlib.sha256(temp_string.encode())
            number = int.from_bytes(hash_object.digest(), byteorder="big")
            short_link = sqids.encode(list(map(int, list(str(number)))))[:5]
            if not Redirect.objects.get_by_short_link(short_link):
                break
            counter += 1

        self.cleaned_data[Redirect.short_link.field.name] = short_link
        del self.cleaned_data["custom_url"]

        return self.cleaned_data


class RedirectFormExtended(RedirectForm):
    links_file = forms.FileField(required=False)

    date_validity_field = forms.DateField(
        label=lazy(
            lambda: Redirect.validity_days.field.verbose_name.capitalize(),
            str,
        ),
        help_text=Redirect.validity_days.field.help_text,
        widget=CustomDateField(format="%Y-%m-%d"),
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
        self.fields["date_validity_field"].widget.update_min_date()

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

        exclude = [
            Redirect.user.field.name,
            Redirect.short_link.field.name,
            Redirect.created_at.field.name,
            Redirect.is_active.field.name,
            Redirect.deactivated_at.field.name,
            Redirect.ip_address.field.name,
            Redirect.create_method.field.name,
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


__all__ = [RedirectForm, RedirectFormExtended, PasswordForm]
