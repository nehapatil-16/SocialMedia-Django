# from django.urls import(
#     include,
#     path
# )
# from django.contrib import admin
# from rest_framework import routers
# from api.views import FriendRequestViewSet, FriendshipViewSet

# # router= routers.DefaultRouter()
# # router.register(r'registration',UserCredentialsViewSet)
# app_name='api'
# userFriendreq_list= FriendRequestViewSet.as_view({
#     'get':'list',
#     #dont want this 
#     'post': 'create',
# })

# userFriendreq_detail = FriendRequestViewSet.as_view({
#     'get':'retrieve',
#     #don't want this
#     'put':'update',
#     'patch':'partial_update',
#     'delete':'destroy',
# })

# #routes define for userProfile
# userFriend_list= FriendshipViewSet.as_view({
#     'get':'list',
#     #dont want this 
#     'post': 'create',
# })
# userFriend_detail= FriendshipViewSet.as_view({
#     'get':'retrieve',
#     #don't want this
#     'put':'update',
#     'patch':'partial_update',
#     'delete':'destroy',
# })

# urlpatterns = [
#     # path('',include(router.urls))
#     path('user-request/',userFriendreq_list,name='userFriendreq-list'),
#     path('user-request/<int:pk>/',userFriendreq_detail,name='userFriendreq-detail'),
#     path('user-friend/',userFriend_list,name='userFriend-list'),
#     path('user-friend/<int:pk>',userFriend_detail,name='userFriend-detail'),
# ]