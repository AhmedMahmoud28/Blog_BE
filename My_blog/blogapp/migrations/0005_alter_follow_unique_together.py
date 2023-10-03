# Generated by Django 4.1.1 on 2023-10-01 16:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blogapp", "0004_alter_tag_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="follow",
            unique_together={("user", "following")},
        ),
    ]
