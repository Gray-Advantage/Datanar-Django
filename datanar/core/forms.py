class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if len(self.visible_fields()) == 1:
            field = self.visible_fields()[0]
            field.field.widget.attrs[
                "class"
            ] = "form-control input-field-only-one"
            if self.errors.get(field.name):
                field.field.widget.attrs["class"] += " is-invalid"
        else:
            for field in self.visible_fields():
                field.field.widget.attrs["class"] = "form-control input-field"
                if self.errors.get(field.name):
                    field.field.widget.attrs["class"] += " is-invalid"


__all__ = [BootstrapFormMixin]
