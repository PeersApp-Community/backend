# Generated by Django 4.1b1 on 2022-07-05 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("peers_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chat",
            options={"ordering": ["pinned", "-updated", "-created"]},
        ),
        migrations.AlterModelOptions(
            name="space",
            options={"ordering": ["pinned", "-updated", "-created"]},
        ),
    ]