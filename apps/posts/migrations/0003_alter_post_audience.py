# Generated by Django 5.0.3 on 2024-03-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_alter_post_audience_postcomment_postlike"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="audience",
            field=models.CharField(
                choices=[
                    ("friends", "Friends"),
                    ("close_friends", "Close Friends"),
                ],
                default="friends",
                max_length=20,
            ),
        ),
    ]
