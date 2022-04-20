"""studysocio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from apps.core.views import frontpage, signup
from apps.feed.views import feed, displayfeed,deletefeed, search
from apps.studysocioprofile.views import studysocioprofile, follow_ssuser, unfollow_ssuser, removefollow_ssuser, \
    send_friend_request, accept_friend_request, followers, follows, edit_profile

from django.contrib.auth import views

from django.conf import settings
from django.conf.urls.static import static

from apps.feed.api import api_add_postfeed, api_like_postfeed

urlpatterns = [
    # admin part
    path('admin/', admin.site.urls),

    # students and teachers registering and accessing system:
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),

    path('feed/', feed, name='feed'),
    path('search/', search, name='search'),
    path('u/<str:username>/', studysocioprofile, name='studysocioprofile'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('u/<str:username>/follow', follow_ssuser, name='follow_ssuser'),
    path('u/<str:username>/unfollow', unfollow_ssuser, name='unfollow_ssuser'),
    path('u/<str:username>/removefollow_ssuser', removefollow_ssuser, name='removefollow_ssuser'),
    path('feed/delete/<int:id>', deletefeed, name='deletefeed'),
    path('displayfeed/', displayfeed, name='displayfeed'),

    path('u/<str:username>/followers', followers, name='followers'),
    path('u/<str:username>/follows', follows, name='follows'),



    path('send_friend_request/<int:userID>', send_friend_request,name='send_friend_request'),
    path('accept_friend_request/<int:userID>', accept_friend_request,name='accept_friend_request'),

    ##api#
    path('api/add_like/', api_like_postfeed, name='api_like_postfeed'),
     #path('api/add_PostFeed/', api_add_postfeed, name='api_add_PostFeed'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
