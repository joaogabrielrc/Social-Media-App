from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from profiles.models import Post, Profile


@login_required(login_url='/signin/')
def index_view(request):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)

  posts = Post.objects.all().order_by('-created_at')

  context = {
    'user_profile': user_profile,
    'posts': posts
  }
  return render(request, 'index.html', context)
