from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserCredential, UserProfile, UserPost, Comment, FriendRequest, Friendship, Report
from datetime import date

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_credential_creation(self):
        user_credential = UserCredential.objects.create(
            username='testuser',
            firstname='Test',
            lastname='User',
            password='testpassword',
            email='test@example.com'
        )
        self.assertEqual(user_credential.username, 'testuser')
        self.assertEqual(user_credential.firstname, 'Test')
        self.assertEqual(user_credential.lastname, 'User')
        self.assertEqual(user_credential.password, 'testpassword')
        self.assertEqual(user_credential.email, 'test@example.com')

    def test_user_profile_creation(self):
        user_profile = UserProfile.objects.create(
            bio='Test bio',
            user=self.user
        )
        self.assertEqual(user_profile.bio, 'Test bio')
        self.assertEqual(user_profile.user, self.user)

    def test_user_post_creation(self):
        user_post = UserPost.objects.create(
            user=self.user,
            text='Test post',
            date_of_Post=date.today()
        )
        self.assertEqual(user_post.user, self.user)
        self.assertEqual(user_post.text, 'Test post')

    def test_comment_creation(self):
        comment = Comment.objects.create(
            user=self.user,
            user_post=UserPost.objects.create(user=self.user, text='Test post', date_of_Post=date.today()),
            content='Test comment'
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.user_post.text, 'Test post')
        self.assertEqual(comment.content, 'Test comment')

    def test_friend_request_creation(self):
        friend_request = FriendRequest.objects.create(
            from_user=self.user,
            to_user=User.objects.create_user(username='testuser2', password='testpassword2'),
            is_accepted=False
        )
        self.assertEqual(friend_request.from_user, self.user)
        self.assertEqual(friend_request.to_user.username, 'testuser2')
        self.assertFalse(friend_request.is_accepted)

    def test_friendship_creation(self):
        friendship = Friendship.objects.create(
            user=self.user,
            follower=User.objects.create_user(username='testuser2', password='testpassword2')
        )
        self.assertEqual(friendship.user, self.user)
        self.assertEqual(friendship.follower.username, 'testuser2')

    def test_report_creation(self):
        user_post = UserPost.objects.create(user=self.user, text='Test post', date_of_Post=date.today())
        report = Report.objects.create(
            user_post=user_post,
            user=self.user,
            reason='Test reason'
        )
        self.assertEqual(report.user_post, user_post)
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.reason, 'Test reason')
