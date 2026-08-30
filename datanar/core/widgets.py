from django import forms
from django.utils import timezone


class DatePickerInput(forms.DateInput):
    input_type = "date"
    format = "%Y-%m-%d"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["min"] = timezone.localdate()
        return context


__all__ = ["DatePickerInput"]
