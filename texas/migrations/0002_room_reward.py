# Generated by Django 4.1.1 on 2022-12-03 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("texas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="room", name="reward", field=models.IntegerField(default=0),
        ),
    ]
