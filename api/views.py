from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
# from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from userCredential.models import Report, UserCredential, UserPost, UserProfile,FriendRequest,Friendship, Comment, Like, Chat
from api.serializers import (
    LikeSerializer,
    ReportSerializer,
    UserCredentialsSerializer, 
    UserPostSerializer,
      UserProfileSerializer,
      FriendRequestSerializer,
      FriendshipSerializer,
      UserPostSerializer,
      UserSerializer,
      CommentSerializer,
      ChatsSerializer
      )
from django.contrib.auth.models import User, auth
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view

class RegisterView(APIView):
    def post(self, request):
        # Extract JSON data from the request body
        data = request.data
        
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
        pending_registration = UserCredential.objects.create(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password=password,
        )
        # Return a success message
        return Response({'success': 'Registration data received and pending approval'}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        # Extract JSON data from the request body
        data = request.data

        # Add validation and error handling if needed
        username = data.get('username')
        print(username)
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Retrieve the token associated with the user
            token = Token.objects.get(user=user)

            # Return user details along with the token
            response_data = {
                'userid': user.id,
                'username': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'token': token.key,
            }
            return Response(response_data, status=status.HTTP_200_OK)

            
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserCredentialsViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def sendRequest(self, request, pk=None):
        user=User.objects.get(pk=pk)# Get the UserCredential instance
        sendRequests = FriendRequest.objects.filter(to_user=user)
        sendRequest_serializer = FriendRequestSerializer(sendRequests, many=True, context={'request': request})
        return Response(sendRequest_serializer.data, status=status.HTTP_200_OK)
    
    def get_non_friend_users(self,request, user_id):
        try:
        # Get the logged-in user
            logged_in_user = User.objects.get(pk=user_id)

        # Get the IDs of users who are friends of the logged-in user
            friend_ids = Friendship.objects.filter(user=logged_in_user).values_list('follower_id', flat=True)

        # Get users who are not friends of the logged-in user
            non_friend_users = User.objects.exclude(
                Q(pk=user_id) | Q(pk__in=friend_ids)
            ).values('id', 'username', 'email')

            return JsonResponse({'users': list(non_friend_users)}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        queryset = UserProfile.objects.all()

        if user:
            queryset = queryset.filter(user=user)

        return queryset

class UserPostViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    queryset=UserPost.objects.all()
    serializer_class=UserPostSerializer
    permission_classes= [permissions.IsAuthenticated]#session authetication

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        queryset = UserPost.objects.all()

        if user:
            queryset = queryset.filter(user=user)

        return queryset

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes= [permissions.IsAuthenticated]#session authetication

class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    # permission_classes= [permissions.IsAuthenticated]#session authetication
    @action(detail=True, methods=['get'])
    def FriendList(self, request, pk=None):
        user=User.objects.get(pk=pk)# Get the User instance
        FriendList = Friendship.objects.filter(user=user)
        FriendList_serializer = FriendshipSerializer(FriendList, many=True, context={'request': request})
        return Response(FriendList_serializer.data, status=status.HTTP_200_OK)
    
class ReportRequestViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        user_post = self.request.query_params.get('user_post', None)

        queryset = Report.objects.all()
        if user:
            queryset = queryset.filter(user=user)
        if user_post:
            queryset = queryset.filter(user_post=user_post)

        return queryset
    # permission_classes= [permissions.IsAuthenticated]#session authetication

class CommentCreateAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request):
        print(request.data)
        user_id = request.data.get('user')
        post_id = request.data.get('user_post')
        content = request.data.get('content')

        try:
            user = User.objects.get(id=user_id)
            post = UserPost.objects.get(id=post_id)
        except (User.DoesNotExist, UserPost.DoesNotExist) as e:
            return Response({'message': 'Invalid user or post ID'}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(user=user, user_post=post, content=content)
        return Response({'message': "Comment Created successfully"}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def get_comments(request):
    post_id = request.query_params.get('user_post')
    if post_id is not None:
        comments = Comment.objects.filter(user_post=post_id)
    else:
        comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

class ChatsViewSet(viewsets.ModelViewSet):
    queryset=Chat.objects.all()
    serializer_class=ChatsSerializer
    permission_classes= [permissions.IsAuthenticated]#session authetication

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        queryset = Chat.objects.all()

        if user:
            queryset = queryset.filter(user=user)
        return queryset

  
class LikeCreateAPIView(viewsets.ModelViewSet):
    # parser_classes = (MultiPartParser, FormParser)

    queryset=Like.objects.all()
    serializer_class=LikeSerializer
  
    def lists(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        liked_data = Like.objects.filter(user=user_id)
        serializer = self.get_serializer(liked_data, many=True)
        return Response(serializer.data)
    