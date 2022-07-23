from django.urls import path

from .views import (
  signup_view, 
  settings_view,
  signin_view, 
  logout_view,
  upload_view
)


urlpatterns = [
  path('signup/', signup_view, name='signup'),
  path('settings/', settings_view, name='settings'),
  path('upload/', upload_view, name='upload'),
  path('signin/', signin_view, name='signin'),
  path('logout/', logout_view, name='logout')
]
