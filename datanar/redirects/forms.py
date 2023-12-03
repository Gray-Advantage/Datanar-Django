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

        for field in self.fields.values():
            field.widget.attrs.update({"placeholder": field.help_text})

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
            if Redirect.objects.get_by_short_link(custom_url):
                self.add_error(
                    "custom_url",
                    ValidationError(_("custom_url_already_use")),
                )
                return None
            self.cleaned_data["short_link"] = custom_url
            del self.cleaned_data["custom_url"]
            return self.cleaned_data

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


__all__ = [RedirectForm]
