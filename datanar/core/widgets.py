__all__ = ("DatePickerInput",)

from typing import Any

from django import forms
from django.utils import timezone


class DatePickerInput(forms.DateInput):
    input_type = "date"
    format = "%Y-%m-%d"

    def get_context(
        self,
        name: str,
        value: Any,
        attrs: dict[str, Any] | None,
    ) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["min"] = timezone.localdate()
        return context
