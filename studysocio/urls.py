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

from apps.announcement.views import announcements, create_announcement, my_announcements, edit_announcement, \
    delete_announcement
from apps.article.api import api_like_article
from apps.article.views import articles, per_article, create_article, article_category, your_articles, delete_articles, \
    my_per_article, edit_article
from apps.classroom.views import create_classroom, edit_classroom, add_classroom_members, add_assignment_grades, \
    add_classroom_assignment, edit_classroom_assignment, edit_assignment_grades, submit_assignment, \
    edit_submit_assignment, add_lesson_materials, edit_lesson_materials, classrooms, classroom_activity, \
    delete_classroom, delete_lesson_materials, leave_classroom, delete_classroom_assignment, view_submit_assignment, \
    remove_classroom_members
from apps.complaint.views import complaints, make_complaint
from apps.core.views import frontpage, signup, password_reset_request
from apps.feed.views import feed, displayfeed, deletefeed, search, replypost, viewreplypost, deletereplyfeed
from apps.groupconversation.views import create_group, add_member, groupconversations, groupconversation, \
    listofgroupmembers, deletegroupmessage, edit_group, removegroupuser, deletegroup
from apps.notification.api import NotificationCheck #getnotification
from apps.notification.views import notifications, notificationsclear
from apps.studysocioprofile.views import studysocioprofile, follow_ssuser, unfollow_ssuser, removefollow_ssuser, \
    send_friend_request, accept_friend_request, followers, follows, edit_profile, deletefeed_profile, \
    deletereplyfeed_profile, user_articles, user_lessons
from apps.directconversation.views import directconversations, directconversation, deletemessage, \
    deletedirectconversations

from django.contrib.auth import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from apps.feed.api import api_add_postfeed, api_like_postfeed, api_display, displayfeed1
from apps.directconversation.api import api_add_message
from apps.videolessons.api import api_like_lesson
from apps.videolessons.views import lessons_category, lessons, create_lesson, per_lesson, your_lessons, edit_lesson, \
    delete_lesson, my_per_lesson

urlpatterns = [
    # admin part
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path(
        'change-password/',auth_views.PasswordChangeView.as_view(template_name='commons/change-password.html',
            success_url='/'
        ),name='change_password'),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='commons/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="commons/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='commons/password/password_reset_complete.html'), name='password_reset_complete'),



    path('complaints/', complaints, name='complaints'),
    path('make_complaint/', make_complaint, name='make_complaint'),

    # students and teachers registering and accessing system:
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),

    path('feed/', feed, name='feed'),
    path('feed/delete/<int:id>', deletefeed, name='deletefeed'),
    path('feed/replypost', replypost, name='replypost'),
    path('feed/replypost/<int:id>/deletereplyfeed/', deletereplyfeed, name='deletereplyfeed'),
    path('feed/viewreplypost/<int:id>', viewreplypost, name='viewreplypost'),
    path('search/', search, name='search'),
    # profie view part
    path('u/<str:username>/studysocioprofile/<int:id>/deletefeed_profile/', deletefeed_profile, name='deletefeed_profile'),
    path('u/<str:username>/studysocioprofile/<int:id>/deletereplyfeed_profile/', deletereplyfeed_profile, name='deletereplyfeed_profile'),


    path('announcements/', announcements, name='announcements'),
    path('announcements/create_announcement/', create_announcement, name='create_announcement'),
    path('announcements/<str:username>/my_announcements/', my_announcements, name='my_announcements'),
    path('announcements/<str:username>/my_announcements/<int:announcement_id>/edit_announcement/', edit_announcement, name='edit_announcement'),
    path('announcements/<str:username>/my_announcements/<int:announcement_id>/delete_announcement', delete_announcement, name='delete_announcement'),


    path('lessons_category/', lessons_category, name='lessons_category'),
    path('lessons_category/create_lesson', create_lesson, name='create_lesson'),
    path('lessons_category/<int:category_id>/lessons/', lessons, name='lessons'),
    path('lessons_category/<int:category_id>/lessons/<int:lesson_id>/per_lesson', per_lesson, name='per_lesson'),
    path('lessons_category/<str:username>/your_lessons', your_lessons, name='your_lessons'),
    path('lessons_category/<str:username>/your_lessons/<int:lesson_id>/edit_lesson/', edit_lesson, name='edit_lesson'),
    path('lessons_category/<str:username>/your_lessons/<int:lesson_id>/delete_lesson/', delete_lesson, name='delete_lesson'),
    path('lessons_category/<str:username>/your_lessons/<int:lesson_id>/my_per_lesson/', my_per_lesson, name='my_per_lesson'),


    path('create_article/', create_article, name='create_article'),

    path('article_category/', article_category, name='article_category'),
    path('article_category/<int:category_id>/articles/', articles, name='articles'),
    path('article_category/<str:user_name>/your_articles/', your_articles, name='your_articles'),
    path('article_category/<str:user_name>/your_articles/<int:article_id>/edit_article/', edit_article, name='edit_article'),
    path('article_category/<str:user_name>/your_articles/<int:article_id>/delete_articles/', delete_articles, name='delete_articles'),
    path('article_category/<int:category_id>/articles/<int:article_id>/per_article/', per_article, name='per_article'),
    path('article_category/<str:user_name>/your_articles/<int:article_id>/my_per_article/', my_per_article, name='my_per_article'),
    path('u/<str:username>/', studysocioprofile, name='studysocioprofile'),
    path('u/<str:username>/user_articles/', user_articles, name='user_articles'),
    path('u/<str:username>/user_lessons/', user_lessons, name='user_lessons'),
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
    path('groupconversations/deletegroup/<int:group_id>', deletegroup, name='deletegroup'),
    path('groupconversations/<int:id>/edit_group/', edit_group, name='edit_group'),
    path('groupconversations/<int:group_id>/add_members/', add_member, name='add_members'),
    path('groupconversations/', groupconversations, name='groupconversations'),
    path('groupconversations/<int:group_id>', groupconversation, name='groupconversation'),
    path('groupconversations/<int:group_id>/listofgroupmembers', listofgroupmembers, name='listofgroupmembers'),
    path('groupconversations/<int:group_id>/delete/<int:message_id>', deletegroupmessage, name='deletegroupmessage'),
    path('groupconversations/<int:group_id>/listofgroupmembers/<int:user_id>/remove/', removegroupuser, name='removegroupuser'),

    ## Classroom
    path('classroom/', classrooms, name='classrooms'),
    path('create_classroom/', create_classroom, name='create_classroom'),
    path('classroom/<int:classroom_id>/delete_classroom/', delete_classroom, name='delete_classroom'),
    path('classroom/<int:classroom_id>/leave_classroom/', leave_classroom, name='leave_classroom'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:user_id>/remove_classroom_members/', remove_classroom_members, name='remove_classroom_members'),
    path('classroom/<int:classroom_id>/classroom_activity/', classroom_activity, name='classroom_activity'),
    path('classroom/<int:classroom_id>/edit_classroom/', edit_classroom, name='edit_classroom'),
    path('classroom/<int:classroom_id>/add_classroom_members/', add_classroom_members, name='add_classroom_members'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:assignment_id>/view_submit_assignment/<int:assignment_grade_id>/edit_assignment_grades/', edit_assignment_grades, name='edit_assignment_grades'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:assignment_id>/add_assignment_grades/', add_assignment_grades, name='add_assignment_grades'),
    path('classroom/<int:classroom_id>/add_classroom_assignment/', add_classroom_assignment, name='add_classroom_assignment'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:assignment_id>/edit_classroom_assignment/', edit_classroom_assignment, name='edit_classroom_assignment'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:assignment_id>/delete_classroom_assignment/', delete_classroom_assignment, name='delete_classroom_assignment'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:assignment_id>/submit_assignment/', submit_assignment, name='submit_assignment'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:assignment_id>/view_submit_assignment/', view_submit_assignment, name='view_submit_assignment'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:assignment_id>/view_submit_assignment/<int:submitassign_id>/edit_submit_assignment/', edit_submit_assignment, name='edit_submit_assignment'),
    path('classroom/<int:classroom_id>/add_lesson_materials/', add_lesson_materials, name='add_lesson_materials'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:lesson_materials_id>/edit_lesson_materials/', edit_lesson_materials, name='edit_lesson_materials'),
    path('classroom/<int:classroom_id>/classroom_activity/<int:lesson_materials_id>/delete_lesson_materials/', delete_lesson_materials, name='delete_lesson_materials'),


    path('send_friend_request/<int:userID>', send_friend_request,name='send_friend_request'),
    path('accept_friend_request/<int:userID>', accept_friend_request,name='accept_friend_request'),

    path('notifications/', notifications, name='notifications'),
    path('notificationsclear/', notificationsclear, name='notificationsclear'),
    path('ajax_notification/', NotificationCheck.as_view()),


    ##api#
    path('api/api_like_article/', api_like_article, name='api_like_article'),
    path('api/api_like_lesson/', api_like_lesson, name='api_like_lesson'),
    path('api/add_like/', api_like_postfeed, name='api_like_postfeed'),
    path('api/api_display/', api_display, name='api_display'),
    path('api/api_add_message/', api_add_message, name='api_add_message'),
    #path('api/noticount/', getnotification, name='getnotification'),
    path('api/displayfeed1/', displayfeed1, name='displayfeed1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
