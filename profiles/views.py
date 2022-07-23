from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from profiles.models import Post, Profile


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
