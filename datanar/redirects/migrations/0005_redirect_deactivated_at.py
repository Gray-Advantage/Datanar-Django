# Generated by Django 4.2.14 on 2024-08-07 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "redirects",
            "0004_redirect_create_method_redirect_ip_address_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="redirect",
            name="deactivated_at",
            field=models.DateTimeField(
                help_text="when_bond_was_deactivated",
                null=True,
                verbose_name="deactivation_time",
            ),
        ),
    ]