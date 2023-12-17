# Generated by Django 4.2.7 on 2023-12-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="avatars/",
                verbose_name="avatar",
            ),
        ),
    ]
