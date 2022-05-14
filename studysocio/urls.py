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
from django.urls import path, include

from apps.article.views import article
from apps.core.views import frontpage, signup
from apps.feed.views import feed, displayfeed, deletefeed, search, replypost, viewreplypost
from apps.groupconversation.views import create_group, add_member, groupconversations, groupconversation, \
    listofgroupmembers
from apps.notification.api import NotificationCheck #getnotification
from apps.notification.views import notifications, notificationsclear
from apps.studysocioprofile.views import studysocioprofile, follow_ssuser, unfollow_ssuser, removefollow_ssuser, \
    send_friend_request, accept_friend_request, followers, follows, edit_profile
from apps.directconversation.views import directconversations, directconversation, deletemessage, \
    deletedirectconversations

from django.contrib.auth import views

from django.conf import settings
from django.conf.urls.static import static

from apps.feed.api import api_add_postfeed, api_like_postfeed, api_display, displayfeed1
from apps.directconversation.api import api_add_message

urlpatterns = [
    # admin part
    path('admin/', admin.site.urls),

    # students and teachers registering and accessing system:
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),

    path('feed/', feed, name='feed'),
    path('feed/delete/<int:id>', deletefeed, name='deletefeed'),
    path('feed/replypost', replypost, name='replypost'),
    path('feed/viewreplypost/<int:id>', viewreplypost, name='viewreplypost'),
    path('search/', search, name='search'),

    path('article/', article, name='article'),
    path('u/<str:username>/', studysocioprofile, name='studysocioprofile'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('u/<str:username>/follow', follow_ssuser, name='follow_ssuser'),
    path('u/<str:username>/unfollow', unfollow_ssuser, name='unfollow_ssuser'),
    path('u/<str:username>/removefollow_ssuser', removefollow_ssuser, name='removefollow_ssuser'),
    path('u/<str:username>/followers', followers, name='followers'),
    path('u/<str:username>/follows', follows, name='follows'),

    #path('displayfeed/', displayfeed, name='displayfeed'),

    # messagings
    path('directconversations/', directconversations, name='directconversations'),
    path('directconversations/<int:user_id>', directconversation, name='directconversation'),
    path('directconversations/<int:user_id>/delete/<int:message_id>', deletemessage, name='deletemessage'),
    path('directconversations/<int:user_id>/deleteall/<int:directconversation_id>', deletedirectconversations, name='deletedirectconversations'),

    path('create_group/', create_group, name='create_group'),
    path('add_members/', add_member, name='add_members'),
    path('groupconversations/', groupconversations, name='groupconversations'),
    path('groupconversations/<int:group_id>', groupconversation, name='groupconversation'),
    path('groupconversations/<int:group_id>/listofgroupmembers', listofgroupmembers, name='listofgroupmembers'),



    path('send_friend_request/<int:userID>', send_friend_request,name='send_friend_request'),
    path('accept_friend_request/<int:userID>', accept_friend_request,name='accept_friend_request'),

    path('notifications/', notifications, name='notifications'),
    path('notificationsclear/', notificationsclear, name='notificationsclear'),
    path('ajax_notification/', NotificationCheck.as_view()),


    ##api#
    path('api/add_like/', api_like_postfeed, name='api_like_postfeed'),
    path('api/api_display/', api_display, name='api_display'),
    path('api/api_add_message/', api_add_message, name='api_add_message'),
    #path('api/noticount/', getnotification, name='getnotification'),
    path('api/displayfeed1/', displayfeed1, name='displayfeed1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
