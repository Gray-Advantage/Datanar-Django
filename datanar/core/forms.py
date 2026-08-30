from django import forms


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if len(self.visible_fields()) == 1:
            attrs = self.visible_fields()[0].field.widget.attrs
            attrs["class"] = "form-control input-field-only-one"
        else:
            for field in self.visible_fields():
                attrs = field.field.widget.attrs

                if isinstance(field.field.widget, forms.CheckboxInput):
                    attrs["class"] = "form-check-input"
                else:
                    attrs["class"] = "form-control input-field"

        self.update_errors_class()

    def update_errors_class(self):
        for field in self.visible_fields():
            if not self.errors.get(field.name):
                continue

            attrs = field.field.widget.attrs
            if "is-invalid" not in attrs["class"]:
                if len(attrs["class"]) > 0:
                    attrs["class"] += " "
                attrs["class"] += "is-invalid"

    def add_error(self, field, error):
        super().add_error(field, error)
        self.update_errors_class()


__all__ = ["BootstrapFormMixin"]
