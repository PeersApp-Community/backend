# Generated by Django 4.1a1 on 2022-06-21 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peers_api", "0009_remove_room_topic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisation",
            name="created",
            field=models.DateTimeField(
                verbose_name=datetime.datetime(2022, 6, 21, 12, 12, 34, 736112)
            ),
        ),
    ]