from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User
from django.db import transaction


class RegistrationTest(APITestCase):
    def setUp(self):
        self.client = self.client_class()
        
    def test_register(self):
        data = {"username" : "test123","email" : 'test@gmail.com',"password": "test12345","password_confirm":"test12345"}
        response = self.client.post('/auth/register/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_register_invalid_username(self):
        data = {"username" : "123","email" : 'test@gmail.com',"password": "test12345","password_confirm":"test12345"}
        response = self.client.post('/auth/register/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_register_invalid_password(self):
        data = {"username" : "test123","email" : 'test@gmail.com',"password": "123","password_confirm":"123"}
        response = self.client.post('/auth/register/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_register_different_passswords(self):
        data = {"username" : "test123","email" : 'test@gmail.com',"password": "test12345","password_confirm":"test3456"}
        response = self.client.post('/auth/register/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_register_invalid_email(self):
        data = {"username" : "test123","email" : 'testgmail.com',"password": "test12345","password_confirm":"test12345"}
        response = self.client.post('/auth/register/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
class LoginTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        self.client = self.client_class()
        
    def test_login_username(self):
        data = {'username_or_email' : 'test','password':'123'}
        response = self.client.post('/auth/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_login_email(self):
        data = {'username_or_email' : 'test@gmail.com','password':'123'}
        response = self.client.post('/auth/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_login_invalid_credentials_email(self):
        data = {'username_or_email' : 'test123@gmail.com','password':'123'}
        response = self.client.post('/auth/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_login_invalid_credentials_username(self):
        data = {'username_or_email' : 'test123','password':'123'}
        response = self.client.post('/auth/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_login_invalid_credentials_password(self):
        data = {'username_or_email' : 'test','password':'12345'}
        response = self.client.post('/auth/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        
class LogoutTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_logout(self):
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
class VerifyAccTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.user.verify_code = '123'
        self.user.save()
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    @transaction.atomic
    def test_verify_code(self):
        data = {"verify_code": "123"}
        self.assertFalse(self.user.is_verified)
        response = self.client.post('/auth/verifyacc/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        
    @transaction.atomic
    def test_verify_code_invalid_code(self):
        data = {"verify_code": "12345"}
        self.assertFalse(self.user.is_verified)
        response = self.client.post('/auth/verifyacc/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verified)