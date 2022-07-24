from django.contrib import admin

from .models import Profile, Post, LikePost, FollowersCount


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ['user']

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
  list_display = ['username']


@admin.register(FollowersCount)
class FollowersCountAdmin(admin.ModelAdmin):
  list_display = ['user', 'follower']
