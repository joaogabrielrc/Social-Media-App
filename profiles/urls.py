from django.urls import path

from .views import (
  signup_view, 
  signin_view, 
  settings_view,
  logout_view,
  like_post_view,
  upload_view,
  profile_view,
  follow_view
)


urlpatterns = [
  path('signup/', signup_view, name='signup'),
  path('signin/', signin_view, name='signin'),
  path('logout/', logout_view, name='logout'),
  path('settings/', settings_view, name='settings'),
  path('like-post/', like_post_view, name='like-post'),
  path('upload/', upload_view, name='upload'),
  path('profile/<str:pk>', profile_view, name='profile'),
  path('follow/', follow_view, name='follow')
]
