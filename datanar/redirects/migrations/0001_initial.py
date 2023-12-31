# Generated by Django 4.2.7 on 2023-12-02 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Redirect",
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
                    "short_link",
                    models.URLField(
                        help_text="shorten_link_to_redirect_to_resource",
                        max_length=50,
                        unique=True,
                        verbose_name="short_link",
                    ),
                ),
                (
                    "long_link",
                    models.URLField(
                        help_text="resource_to_which_short_link_lead",
                        max_length=2000,
                        verbose_name="long_link",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="when_bond_was_create",
                        verbose_name="creation_time",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        help_text="password_that_will_requested_to_redirect",
                        max_length=128,
                        verbose_name="password",
                    ),
                ),
                (
                    "validity_days",
                    models.PositiveIntegerField(
                        default=90,
                        help_text="how_many_day_link_will_be_valid",
                        null=True,
                        verbose_name="valid_day_number",
                    ),
                ),
                (
                    "validity_clicks",
                    models.PositiveIntegerField(
                        default=None,
                        help_text="how_many_click_on_link_will_be_valid",
                        null=True,
                        verbose_name="valid_click_number",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="user_who_create_bond",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
        ),
    ]
