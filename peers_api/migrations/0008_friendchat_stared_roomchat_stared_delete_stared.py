# Generated by Django 4.1a1 on 2022-06-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peers_api", "0007_status_alter_room_topic_delete_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="friendchat",
            name="stared",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="roomchat",
            name="stared",
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name="Stared",
        ),
    ]