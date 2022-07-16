# Generated by Django 4.1b1 on 2022-07-16 15:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("extras", "0013_alter_book_saved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="saved",
            field=models.ManyToManyField(
                blank=True, related_name="saved_books", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]