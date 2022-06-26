# Generated by Django 4.1a1 on 2022-06-26 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("peers_api", "0002_alter_chat_unique_together"),
    ]

    operations = [
        migrations.RenameField(
            model_name="spacemsg",
            old_name="body",
            new_name="message",
        ),
        migrations.AlterField(
            model_name="space",
            name="topic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="peers_api.topic",
            ),
        ),
    ]
