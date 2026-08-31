__all__ = ("BootstrapFormMixin",)

from typing import Any

from django import forms


class BootstrapFormMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        visible_fields = self.visible_fields()
        is_single_field = len(visible_fields) == 1

        for field in visible_fields:
            widget = field.field.widget
            if is_single_field:
                widget.attrs["class"] = "form-control input-field-only-one"
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            else:
                widget.attrs["class"] = "form-control input-field"

        self.update_errors_class()

    def update_errors_class(self) -> None:
        for field in self.visible_fields():
            if not self.errors.get(field.name):
                continue

            widget = field.field.widget
            widget_classes = widget.attrs["class"]

            if "is-invalid" not in widget_classes:
                if len(widget_classes) > 0:
                    widget_classes += " "
                widget_classes += "is-invalid"
                widget.attrs["class"] = widget_classes

    def add_error(self, field: str | None, error: Any) -> None:
        super().add_error(field, error)
        self.update_errors_class()
