from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from itertools import chain

from profiles.models import FollowersCount, Post, Profile, LikePost


def signup_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    if password == password2:    
      if User.objects.filter(email=email).exists():
        messages.info(request, 'Email taken')
        return redirect('signup')
      elif User.objects.filter(username=username).exists():
        messages.info(request, 'Username taken')
        return redirect('signup')
      else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user_login = authenticate(username=username, password=password)
        login(request, user_login)

        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('settings')
    else: 
      messages.info(request, 'Password Not Matching')
      return redirect('signup')
  else:
    return render(request, 'signup.html')


def signin_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']  

    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      messages.info(request, 'Credentials Invalid')
      return redirect('signin')
  else:    
    return render(request, 'signin.html')


@login_required(login_url='/signin/')
def logout_view(request):
  logout(request)
  return redirect('signin')


@login_required(login_url='/signin/')
def settings_view(request):  
  try:
    user_profile = Profile.objects.get(user=request.user)
  except:
    user_profile = None

  if request.method == 'POST':
    if request.FILES.get('image') is None:
      image = user_profile.profileimg
      bio = request.POST['bio']
      location = request.POST['location']

      user_profile.profileimg = image
      user_profile.bio = bio
      user_profile.location = location
      user_profile.save()
    else:
      image = request.FILES.get('image')
      bio = request.POST['bio']
      location = request.POST['location']

      user_profile.profileimg = image
      user_profile.bio = bio
      user_profile.location = location
      user_profile.save()

  context = {
    'user_profile': user_profile
  }
  return render(request, 'setting.html', context)


@login_required(login_url='/signin/')
def upload_view(request):
  if request.method == 'POST':
    user = request.user.username
    image = request.FILES.get('image_upload')
    caption = request.POST['caption']
    new_post = Post.objects.create(user=user, image=image, caption=caption)
    new_post.save()
  return redirect('/')  


@login_required(login_url='/signin/')
def like_post_view(request):
  username = request.user.username
  post_id = request.GET.get('post_id')  

  post = Post.objects.get(id=post_id)
  
  like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

  if like_filter is None:
    new_like = LikePost.objects.create(post_id=post_id, username=username)
    new_like.save()
    post.no_of_likes += 1
    post.save()
    return redirect('/')
  else:
    like_filter.delete()
    post.no_of_likes -= 1
    post.save()
    return redirect('/')


@login_required(login_url='/signin/')
def profile_view(request, pk=None):
  user_object = User.objects.get(username=pk)
  user_profile = Profile.objects.get(user=user_object)
  user_posts = Post.objects.filter(user=pk).order_by('-created_at')
  user_post_length = len(user_posts)

  follower = request.user.username
  user = pk

  if FollowersCount.objects.filter(follower=follower, user=user).first():
    button_text = 'Unfollow'
  else:
    button_text = 'Follow'
    
  user_followers = len(FollowersCount.objects.filter(user=pk))
  user_following = len(FollowersCount.objects.filter(follower=pk))

  context = {
    'user_object': user_object,
    'user_profile': user_profile,
    'user_posts': user_posts,
    'user_post_length': user_post_length,
    'button_text': button_text,
    'user_followers': user_followers,
    'user_following': user_following
  }

  return render(request, 'profile.html', context)


@login_required(login_url='/signin/')
def follow_view(request):
  if request.method == 'POST':
    follower = request.POST['follower']
    user = request.POST['user']

    if FollowersCount.objects.filter(follower=follower, user=user).first():
      delete_follower = FollowersCount.objects.get(follower=follower, user=user)
      delete_follower.delete()    
    else:
      new_follower = FollowersCount.objects.create(follower=follower, user=user)
      new_follower.save()

    return redirect('/profile/' + user)   
  return redirect('/')


@login_required(login_url='/signin/')
def search_view(request):
  context = {}
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)

  if request.method == 'POST':
    username = request.POST['username']
    username_object = User.objects.filter(username__icontains=username)

    username_profile = []
    username_profile_list = []

    for users in username_object:
      username_profile.append(users.id)

    for ids in username_profile:
      profile_lists = Profile.objects.filter(id_user=ids)
      username_profile_list.append(profile_lists)

    username_profile_list = list(chain(*username_profile_list))

    context = {
      'user_profile': user_profile,
      'username_profile_list': username_profile_list
    }

  return render(request, 'search.html', context)
