from django.contrib import admin

from userCredential.models import (
    Comment,
    Report,
    UserCredential, 
    UserPost,
    Media,
    UserProfile,
    FriendRequest,
    Friendship,
    Like,
    Chat,
    UserStory,
    )
from django.contrib.auth.models import User

def approve_registration(modeladmin, request, queryset):
    for pending_registration in queryset:
        # Create a new user based on the pending registration data
        new_user = User.objects.create_user(
            username=pending_registration.username,
            email=pending_registration.email,
            password=pending_registration.password,
            first_name=pending_registration.firstname,
            last_name=pending_registration.lastname,
            # Add other fields as needed
        )
        pending_registration.delete()

        user_profile = UserProfile(
            profilepic='',
            bio='',
            friends=0,
            post_count=0,
            user= new_user,
        )
        user_profile.save()

approve_registration.short_description = "Approve selected registration requests"

@admin.register(UserCredential)
class PendingRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'firstname', 'lastname')
    actions = [approve_registration]

admin.site.register(UserProfile)
admin.site.register(UserPost)
admin.site.register(Media)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Like)
admin.site.register(Chat)
admin.site.register(UserStory)