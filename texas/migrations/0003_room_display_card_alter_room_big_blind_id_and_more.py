# Generated by Django 4.1.1 on 2022-12-03 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("texas", "0002_room_reward"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="display_card",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="room",
            name="big_blind_id",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="room", name="dealer_id", field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="room",
            name="small_blind_id",
            field=models.IntegerField(default=0),
        ),
    ]
