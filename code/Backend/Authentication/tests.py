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
        
class UsersListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_user_list(self):
        response = self.client.get('/auth/users/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        

class UserObjectTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_user(self):
        response = self.client.get(f'/auth/users/{self.user.id}/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_get_user_list_not_exists(self):
        response = self.client.get('/auth/user/404',format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        

class FollowerssFollowingTesst(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_followers_following(self):
        response = self.client.get('/auth/followersfollowinguser/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class ChangeCustomNameTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    @transaction.atomic
    def test_change_custom_name(self):
        data = {'custom_name' : 'test123'}
        response = self.client.post('/auth/changecustomname/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual('test123',self.user.custom_name)
        
    @transaction.atomic
    def test_change_custom_name_too_short(self):
        data = {'custom_name' : 'tt'}
        response = self.client.post('/auth/changecustomname/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual('tt',self.user.custom_name)
        
    @transaction.atomic
    def test_change_custom_name_taken(self):
        user_test_2 = User.objects.create_user(username='test2',password='123',email='test2@gmail.com')
        data = {'custom_name' : 'test2'}
        response = self.client.post('/auth/changecustomname/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual('test2',self.user.custom_name)
        
        
class FollowUserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    @transaction.atomic
    def test_follow_user(self):
        user_test_2 = User.objects.create_user(username='test2',password='123',email='test2@gmail.com')
        response = self.client.post(f'/auth/followuser/{user_test_2.id}/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(1,len(self.user.following.all()))
        
    @transaction.atomic
    def test_follow_not_exist_user(self):
        response = self.client.post('/auth/followuser/404/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.user.refresh_from_db()
        self.assertEqual(0,len(self.user.following.all()))
        
    @transaction.atomic
    def test_follow_yourself(self):
        response = self.client.post(f'/auth/followuser/{self.user.id}/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertEqual(0,len(self.user.following.all()))
    
    @transaction.atomic
    def test_unfollow_user(self):
        user_test_2 = User.objects.create_user(username='test2',password='123',email='test2@gmail.com')
        self.user.following.add(user_test_2)
        self.user.refresh_from_db()
        response = self.client.post(f'/auth/followuser/{user_test_2.id}/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(0,len(self.user.following.all()))



class TestNoPermissionURL(APITestCase):
    def setUp(self):
        self.client = self.client_class() 
        
    def test_logout_url(self):
        response = self.client.post('/auth/logout/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_verifyacc_url(self):
        response = self.client.post('/auth/verifyacc/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_users_url(self):
        response = self.client.get('/auth/users/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_users_iduser_url(self):
        response = self.client.get(f'/auth/users/1/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_followersfollowinguser_url(self):
        response = self.client.get('/auth/followersfollowinguser/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_changecustomname_url(self):
        response = self.client.post('/auth/changecustomname/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_followuser_iduser_url(self):
        response = self.client.post('/auth/followuser/1/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    