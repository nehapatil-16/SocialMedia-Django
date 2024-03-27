from django.urls import(
    include,
    path
)
from django.contrib import admin
from rest_framework import routers
# from api.views import *
from api.views import (
    UserViewSet,
    ReportRequestViewSet,
    UserCredentialsViewSet, 
    UserProfileViewSet,
    FriendshipViewSet,
    FriendRequestViewSet,
    UserPostViewSet,
    CommentCreateAPIView,
    LikeCreateAPIView,
    get_comments,
    ChatsViewSet,
    MediaListView,
    UserStoryViewSet,
    check_user_exists,
    update_password
)
from userCredential import views
from api import views
from rest_framework.routers import DefaultRouter
# from api.views import get_all_users, get_user_by_id

router = DefaultRouter()
router.register(r'user-credentials', UserCredentialsViewSet, basename='user-credentials')

app_name='api'

authuser_list = UserViewSet.as_view({
    'get':'list',
    'post':'create',
})

authuser_detail = UserViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})

user_list= UserCredentialsViewSet.as_view({
    'get':'list',
    'post': 'create',
})

user_detail = UserCredentialsViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})

#routes define for userProfile
userProfile_list= UserProfileViewSet.as_view({
    'get':'list',
    'post': 'create',
})
userProfile_detail= UserProfileViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})
userFriendreq_list= FriendRequestViewSet.as_view({
    'get':'list',
    'post': 'create',
})

userFriendreq_detail = FriendRequestViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})

#routes define for userProfile
userFriend_list= FriendshipViewSet.as_view({
    'get':'list',
    'post': 'create',
})
userFriend_detail= FriendshipViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})

userpost_list= UserPostViewSet.as_view({
    'get':'list',
    'post': 'create',
})
userpost_detail = UserPostViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})

Report_detail= ReportRequestViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})
Report_list= ReportRequestViewSet.as_view({
   'get':'list',
    'post': 'create',
})
comments = CommentCreateAPIView.as_view({
    'get':'retrieve',
    'post': 'create',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})
# get_comments = CommentCreateAPIView.as_view({
#     'get':'list',
#     'post': 'create',
# })
comments_list= CommentCreateAPIView.as_view({
    'get':'list',
    'post': 'create',
})

likes_list = LikeCreateAPIView.as_view({
    'get':'retrieve',
    'post': 'create',
})
likes_detail= LikeCreateAPIView.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})
chats_list= ChatsViewSet.as_view({
    'get':'list',
    'post': 'create',
})
chats_detail= ChatsViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})
Story_list = UserStoryViewSet.as_view({
    'get':'retrieve',
    'post': 'create',
})
story_detail= UserStoryViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy',
})

urlpatterns = [
    path('user-profile/',userProfile_list,name='userProfile-list'),
    path('user-profile/<int:pk>',userProfile_detail,name='userProfile-detail'),
    path('user-request/',userFriendreq_list,name='userFriendreq-list'),
    path('user-request/<int:pk>/',userFriendreq_detail,name='userFriendreq-detail'),
    path('user-friend/',userFriend_list,name='userFriend-list'),
    path('user-friend/<int:pk>',userFriend_detail,name='userFriend-detail'),
    path('userpost/',userpost_list,name='userpost_list'),
    path('userpost/<int:pk>',userpost_detail,name='userpost_detail'),
    path('media/', MediaListView.as_view({'get': 'list', 'post': 'create'}), name='media_list'),

    path('report/<int:pk>/',Report_detail,name='Report_detail'),
    path('report/',Report_list,name='Report_list'),
    path('user/<int:pk>/send-request/', UserCredentialsViewSet.as_view({'get': 'sendRequest'}), name='user-credentials-send-request'),
    path('nonfriendUser/<int:user_id>/', UserCredentialsViewSet.as_view({'get': 'get_non_friend_users'}), name='non-friend-users'),
    path('user/<int:pk>/FriendList/', FriendshipViewSet.as_view({'get': 'FriendList'}), name='user-credentials-FriendList'),
    path('user/<int:pk>/FriendUsername/', FriendshipViewSet.as_view({'get': 'FriendUsername'}), name='user-credentials-FriendUsername'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('authuser/',authuser_list, name='user-list'),
    path('authuser/<int:pk>/', authuser_detail, name='user-detail'),
    path('comments/', comments, name='comment-create'),
    path('comments-list/', comments_list, name='comments_list'),
    # path('likes/', likes_list, name='likes-list'),
    # path('liked-posts/<int:user_id>/', LikeCreateAPIView.as_view({'get': 'get'}), name='liked-posts'),
    path('likes/', LikeCreateAPIView.as_view({'get': 'list', 'post': 'create'}), name='likes-list'),
    path('likes/<int:pk>', likes_detail, name='likes_detail'),
    path('chats/',chats_list,name='chats_list'),
    path('chats/<int:pk>', chats_detail, name='chats_detail'),
    path('get-comments/', get_comments, name='get-comment'),
    path('comments/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('liked-posts/<int:user_id>/', LikeCreateAPIView.as_view({'get': 'lists'}), name='liked-posts'),

    path('userstory/', UserStoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='Story_list'),
    path('story/<int:user_id>/', UserStoryViewSet.as_view({'get': 'lists'}), name='liked-posts'),
    path('userstory/<int:pk>',story_detail,name='story_detail'),
    path('check-user-exists/', check_user_exists, name='check_user_exists'),
    path('update-password/', update_password, name='update_password'),

]