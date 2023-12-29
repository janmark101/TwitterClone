from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from django.contrib.auth import authenticate, logout
from .serializers import UserSerializer

# Create your views here.
class Login(APIView):
    permission_classes=()
    
    def get(self,request):
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
        print(request.user.is_authenticated)
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            return Response({'message':'Logged out succesfully!'},status=status.HTTP_200_OK)
        except Token.DoesNotExists:
            pass
        return Response({'error':'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)  
    
class Register(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer  