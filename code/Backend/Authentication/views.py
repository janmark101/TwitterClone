from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, logout
from .serializers import UserSerializer, UserLessInfoSerializer
from .emails import send_verify_email
from .models import User
from django.shortcuts import get_object_or_404

# Create your views here.
class Login(APIView):
    permission_classes=()
    
    def post(self,request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')
        
        if username_or_email is None or password is None: 
            return Response({'error' : 'You must insert username or email and password!'},status=status.HTTP_400_BAD_REQUEST) 
        
        user = authenticate(username=username_or_email,password=password) # jest to logowanie za pomoca email albo ussername 
        
        if not user:
            return Response({'error':'Invalid credentials!'},status=status.HTTP_400_BAD_REQUEST)
        
        token,created = Token.objects.get_or_create(user=user)
        return Response({'message' : 'Logged in succesfully!','token' : token.key,'user_id':user.id,'username' : user.username,'custom_name': user.custom_name}, status=status.HTTP_200_OK)
    
class Logout(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def post(self,request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            return Response({'message':'Logged out succesfully!'},status=status.HTTP_200_OK)
        except Token.DoesNotExists:
            pass
        return Response({'error':'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)  
    
    
    
class Register(APIView):
    authentication_classes = ()
    permission_classes = ()
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_verify_email(serializer.data['email'])
            return Response({'message': 'Succesfully registered. Verify your email!'},status=status.HTTP_201_CREATED)
        return Response({'error': 'Registration failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 

class VerifyAccount(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def post(self,request):
        user = request.user
        if request.data['verify_code'] == user.verify_code:
            user.is_verified = True
            user.verify_code = ''
            user.save()
            return Response({'message':'Your account has been activated!'},status=status.HTTP_200_OK)  
        return Response({'error':'Something went wrong! Try again.'},status=status.HTTP_400_BAD_REQUEST)  
    
 #return list of all users
class UsersListView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

#return one user 
class UserObjectView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request,pk):
        users = get_object_or_404(User,pk=pk)
        serializer = UserSerializer(users,many=False)
        return Response(serializer.data)
    
 # return list of following and followers for user
class FollowersFollowingForUser(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(sself,request):
        user = request.user
        following = user.following.all()
        followers = user.followers.prefetch_related('following')
        following_serializer = UserLessInfoSerializer(following,many=True).data
        followers_serializer = UserLessInfoSerializer(followers,many=True).data
        followers_following = [{
            'following' : following_serializer,
            'following_count' : len(following_serializer),
            'followers' : followers_serializer,
            'followers_count' : len(followers_serializer)
            }]
        return Response(followers_following,status=status.HTTP_200_OK)
    
#api to change users custom name
class ChangeCustomNameView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def post(self,request):
        custom_name = request.data['custom_name']
        if len(custom_name) <= 4 or custom_name.isdigit():
            return Response({'error': 'Nickname must contain at least 5 characters and cannot consist of only numbers!'},status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(custom_name=custom_name).exists():
            return Response({'error': 'Nickname is already taken. Choose a different one.'},status=status.HTTP_400_BAD_REQUEST)
        else :
            user = request.user
            user.custom_name = custom_name
            user.save()
            return Response({'message': 'Changed succesfully!'},status=status.HTTP_200_OK)
    
   #api to follow users
class FollowUserView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def post(self,request,pk):
        user_to_follow = get_object_or_404(User,pk=pk)
        user = request.user
        
        if user == user_to_follow:
            return Response({'error' : 'You can not follow yourself!'},status=status.HTTP_400_BAD_REQUEST)
        
        elif user_to_follow in user.following.all():
            user.following.remove(user_to_follow)
            return Response({'message' : 'Unfolowed user.'},status=status.HTTP_200_OK)
        
        user.following.add(user_to_follow)
        return Response({'message' : 'User followed.'},status=status.HTTP_200_OK)