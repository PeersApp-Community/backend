# Generated by Django 4.1b1 on 2022-06-30 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("peers_api", "0002_alter_space_archived_alter_space_pinned"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mytask",
            name="user",
        ),
        migrations.RemoveField(
            model_name="spacetask",
            name="space",
        ),
        migrations.RemoveField(
            model_name="story",
            name="user",
        ),
        migrations.DeleteModel(
            name="Library",
        ),
        migrations.DeleteModel(
            name="MyTask",
        ),
        migrations.DeleteModel(
            name="SpaceTask",
        ),
        migrations.DeleteModel(
            name="Story",
        ),
    ]
