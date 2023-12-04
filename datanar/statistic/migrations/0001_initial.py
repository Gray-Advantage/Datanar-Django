# Generated by Django 4.2.7 on 2023-12-04 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("redirects", "0002_alter_redirect_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Click",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "clicked_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="redirect_time"
                    ),
                ),
                (
                    "os",
                    models.TextField(
                        help_text="operating_system_from_which_redirect_was_made",
                        null=True,
                        verbose_name="os",
                    ),
                ),
                (
                    "browser",
                    models.TextField(
                        help_text="browser_from_which_redirect_was_made",
                        null=True,
                        verbose_name="browser",
                    ),
                ),
                ("country", models.TextField(null=True, verbose_name="country")),
                ("city", models.TextField(null=True, verbose_name="city")),
                ("referrer", models.TextField(null=True)),
                (
                    "redirect",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="redirects.redirect",
                    ),
                ),
            ],
        ),
    ]
