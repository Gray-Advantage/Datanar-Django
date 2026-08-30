import io

from django.core.management import call_command
from django.test import TestCase


class MigrationsTest(TestCase):
    def test_no_missing_migrations(self):
        output = io.StringIO()

        try:
            call_command(
                "makemigrations",
                check=True,
                dry_run=True,
                verbosity=1,
                stdout=output,
            )
        except SystemExit:
            self.fail(
                "Модели изменились, но миграции не созданы. "
                "Выполните makemigrations и закоммитьте результат:\n"
                + output.getvalue(),
            )


__all__ = ["MigrationsTest"]
