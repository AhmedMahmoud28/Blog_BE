# Generated by Django 4.1.1 on 2023-09-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tag",
            name="post",
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(to="blogapp.tag"),
        ),
        migrations.DeleteModel(
            name="BlogSection",
        ),
    ]
