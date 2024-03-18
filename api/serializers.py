from rest_framework import serializers
from userCredential.models import FriendRequest, Friendship, Report, UserCredential, UserPost, Comment,UserProfile, Like, Chat
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields="__all__"

class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserCredential
        fields="__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields="__all__"

class  UserPostSerializer(serializers.ModelSerializer):
    media=serializers.FileField(required=False)
    class Meta:
        model=UserPost
        fields="__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = ['user', 'user_post', 'content']
        fields= "__all__"  

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields= "__all__"  

class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields= "__all__"  

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'is_accepted', 'created_at']
        read_only_fields = ['created_at']

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'user', 'follower', 'created_at']
        read_only_fields = ['created_at']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
       