# Generated by Django 5.0.3 on 2024-03-08 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("friends", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="friend",
            name="is_close_friend",
            field=models.BooleanField(default=False),
        ),
    ]