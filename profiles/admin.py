from django.contrib import admin

from .models import Profile, Post


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ['user']
