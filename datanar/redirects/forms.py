import hashlib

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from sqids import Sqids

from core.forms import BootstrapFormMixin
from redirects.models import Redirect


sqids = Sqids()


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
            if first:
                first = False
            else:
                field.widget.attrs["class"] += " mb-2"

    def __str__(self):
        return f"{self.password}"

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

    def clean(self):
        custom_url = self.cleaned_data.get("custom_url")

        if custom_url:
            all_good = True

            if "/" in custom_url:
                self.add_error(
                    "custom_url",
                    ValidationError(_("custom_url_should_not_have_slash")),
                )
                all_good = False
            if Redirect.objects.get_by_short_link(custom_url):
                self.add_error(
                    "custom_url",
                    ValidationError(_("custom_url_already_use")),
                )
                all_good = False

            if all_good:
                self.cleaned_data["short_link"] = custom_url
                del self.cleaned_data["custom_url"]
                return self.cleaned_data
            return None

        counter = 0
        string = self.cleaned_data["long_link"]
        while True:
            temp_string = f"{string}{counter}" if counter > 0 else string
            hash_object = hashlib.sha256(temp_string.encode())
            number = int.from_bytes(hash_object.digest(), byteorder="big")
            short_link = sqids.encode(list(map(int, list(str(number)))))[:5]
            if not Redirect.objects.get_by_short_link(short_link):
                break
            counter += 1

        self.cleaned_data["short_link"] = short_link
        del self.cleaned_data["custom_url"]
        return self.cleaned_data


class RedirectFormExtended(RedirectForm):
    links_file = forms.FileField(required=False)

    field_order = [
        Redirect.long_link.field.name,
        "custom_url",
        Redirect.password.field.name,
        Redirect.validity_days.field.name,
        Redirect.validity_clicks.field.name,
        "links_file",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["links_file"].widget.attrs["class"] = "d-none"
        self.fields["links_file"].widget.attrs["accept"] = ".txt, .xlsx"

    def clean(self):
        if self.cleaned_data["links_file"]:
            self.cleaned_data["long_link"] = "https://some.url.com/"
        return super().clean()

    class Meta(RedirectForm.Meta):
        fields = [
            Redirect.long_link.field.name,
            Redirect.password.field.name,
            Redirect.validity_days.field.name,
            Redirect.validity_clicks.field.name,
        ]

        exclude = [
            Redirect.user.field.name,
            Redirect.short_link.field.name,
            Redirect.created_at.field.name,
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
