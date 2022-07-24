from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from itertools import chain
import random

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
    feed_lists = Post.objects.filter(user=usernames).order_by('-created_at')
    feed.append(feed_lists)

  feed_list = list(chain(*feed))

  # posts = Post.objects.all().order_by('-created_at')

  all_users = User.objects.all()
  user_following_all = []

  for user in user_following:
    user_list = User.objects.get(username=user.user)
    user_following_all.append(user_list)

  new_suggest_list = [x for x in list(all_users) if (x not in list(user_following_all))]
  current_user = User.objects.filter(username=request.user.username)
  final_suggestions_list = [x for x in list(new_suggest_list) if (x not in list(current_user))]

  random.shuffle(final_suggestions_list)

  username_profile = []
  username_profile_list = []

  for users in final_suggestions_list:
    username_profile.append(users.id)
  
  for ids in username_profile:
    profile_lists = Profile.objects.filter(id_user=ids)
    username_profile_list.append(profile_lists)

  suggestions_username_profile_list = list(chain(*username_profile_list))

  context = {
    'user_profile': user_profile,
    'posts': feed_list,
    'suggestions_username_profile_list': suggestions_username_profile_list[:4]
  }
  return render(request, 'index.html', context)
