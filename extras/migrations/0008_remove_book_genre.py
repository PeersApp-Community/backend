# Generated by Django 4.1b1 on 2022-07-15 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0007_remove_book_private_book_public"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="genre",
        ),
    ]
