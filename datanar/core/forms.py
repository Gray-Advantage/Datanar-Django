from django import forms


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if len(self.visible_fields()) == 1:
            self.visible_fields()[0].field.widget.attrs[
                "class"
            ] = "form-control input-field-only-one"
        else:
            for field in self.visible_fields():
                field.field.widget.attrs["class"] = "form-control input-field"
                if isinstance(field.field.widget, forms.CheckboxInput):
                    field.field.widget.attrs["class"] = "form-check-input"

        self.update_errors_class()

    def update_errors_class(self):
        for field in self.visible_fields():
            if self.errors.get(field.name):
                if "is-invalid" not in field.field.widget.attrs["class"]:
                    field.field.widget.attrs["class"] += " is-invalid"

    def add_error(self, field, error):
        super().add_error(field, error)
        self.update_errors_class()


__all__ = [BootstrapFormMixin]
