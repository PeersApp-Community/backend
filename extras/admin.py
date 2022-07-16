from django.contrib import admin
from .models import Book, SpaceTask, MyTask, Library, Story

# Register your models here.


class SpaceTaskInline(admin.TabularInline):
    model = SpaceTask
    min_num = 0
    max_num = 10


class StoryInline(admin.TabularInline):
    model = Story
    min_num = 0
    max_num = 10


class MyTaskInline(admin.TabularInline):
    model = MyTask
    min_num = 0
    max_num = 10


class LibraryInline(admin.TabularInline):
    model = Library
    min_num = 0
    max_num = 10


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["creator", "id", "title","public", "author"]
