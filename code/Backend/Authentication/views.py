from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from django.contrib.auth import authenticate, logout
from .serializers import UserSerializer
from .emails import send_verify_email

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

