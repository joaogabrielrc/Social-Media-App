from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from itertools import chain

from profiles.models import FollowersCount, Post, Profile


@login_required(login_url='/signin/')
def index_view(request):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)
  user_following_list = []
  feed = []
  user_following = FollowersCount.objects.filter(follower=request.user.username)

  for users in user_following:
    user_following_list.append(users.user)

  for usernames in user_following_list:
    feed_lists = Post.objects.filter(user=usernames)
    feed.append(feed_lists)

  feed_list = list(chain(*feed))

  posts = Post.objects.all().order_by('-created_at')

  context = {
    'user_profile': user_profile,
    'posts': feed_list,
  }
  return render(request, 'index.html', context)
