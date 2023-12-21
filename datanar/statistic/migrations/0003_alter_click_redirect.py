# Generated by Django 4.2.7 on 2023-12-08 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("redirects", "0002_alter_redirect_options"),
        ("statistic", "0002_alter_click_redirect"),
    ]

    operations = [
        migrations.AlterField(
            model_name="click",
            name="redirect",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="redirects.redirect",
            ),
        ),
    ]
