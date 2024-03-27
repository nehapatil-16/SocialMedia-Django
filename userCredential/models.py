from django.db import models
from datetime import date
from django.utils import timezone 
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver 
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# Create your models here.
class UserCredential(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=30, default='')
    lastname = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=15)
    email = models.EmailField(max_length=20)
    is_approved = models.BooleanField(default=False)  # Field to indicate approval status
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M')
    date_of_birth = models.DateField(default=date(1900, 1, 1))

    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserProfile(models.Model):
    profilepic = models.ImageField(upload_to='static/media/', blank=True, null=True)
    bio = models.TextField(blank=True)
    friends = models.PositiveIntegerField(default=0)
    post_count = models.PositiveIntegerField(default=0)
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=0
    )
    
class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    # media = models.FileField(upload_to='static/media/', blank=True, null=True)
    date_of_post = models.DateField(default=date(1900, 1, 1))

    def __str__(self):
        return f"Post by {self.user.username}"

class Media(models.Model):
    post = models.ForeignKey(UserPost, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='static/media/', blank=True, null=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='chats_username', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30, default='')
    chats = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} - {self.username.username}'

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2')
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"Report for Post {self.user_post} by User {self.user.id}"
    
class UserStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to='static/story/', blank=True, null=True)
    date_of_Post = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"Post by {self.user.username}"
    
