from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Tweet
from Authentication.models import User


class OnlyTweetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 

    def test_get_tweets(self):
        response = self.client.get('/api/tweets/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_create_tweet(self):
        data = {'content' : 'test tweet'}
        response = self.client.post('/api/tweets/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_error_creating_tweet(self):
        response = self.client.post('/api/tweets/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        
class FullTweetView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_full_tweets(self):
        response = self.client.get('/api/fullapi/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        

class UserTweetsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_user_tweets(self):
        response = self.client.get('/api/userstweets/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        

class TweetsFromFollowedTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_tweets_from_followed(self):
        response = self.client.get('/api/tweetsfromfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class AllTweetsLikedCommentedFromFollowedTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_tweets_liked_commented(self):
        response = self.client.get('/api/tweetslinkedwithfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class UserRetweetedTweetsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_user_retweets(self):
        response = self.client.get('/api/userretweetedtweets/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        

class TweetObjectView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        self.tweet = Tweet.objects.create(content='test',user=self.user)
        
    def test_get_tweet(self):
        response = self.client.get(f'/api/tweets/{self.tweet.id}/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_delete_tweet(self):
        response = self.client.delete(f'/api/tweets/{self.tweet.id}/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_delete_not_existing_tweet(self):
        response = self.client.delete('/api/tweets/404/',format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_delete_not_your_tweet(self):
        user_temp = User.objects.create_user(username='test_temp',password='123',email='testtemp@gmail.com')
        tweet_temp = Tweet.objects.create(content='test',user=user_temp)
        response = self.client.delete(f'/api/tweets/{tweet_temp.id}/',format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
class RetweetView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        self.tweet = Tweet.objects.create(content='test',user=self.user)
        
    def test_retweet(self):
        response = self.client.post(f'/api/retweet/{self.tweet.id}/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(1,len(self.tweet.retweets.all()))
        
    def test_retweet_not_existing_tweet(self):
        response = self.client.post('/api/retweet/404/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        

class TestNoPermissionURLS(APITestCase):
    def setUp(self):
        self.client = self.client_class() 
        
    def test_get_tweets_url(self):
        response = self.client.get('/api/tweets/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_post_tweets_url(self):
        response = self.client.post('/api/tweets/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_fullapi_url(self):
        response = self.client.post('/api/fullapi/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_userstweets_url(self):
        response = self.client.get('/api/userstweets/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_tweetsfromfollowed_url(self):
        response = self.client.get('/api/tweetsfromfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_tweetslinkedwithfollowed_url(self):
        response = self.client.get('/api/tweetslinkedwithfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_userretweetedtweets_url(self):
        response = self.client.get('/api/userretweetedtweets/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_tweet_idtweet_url(self):
        response = self.client.get('/api/tweets/1/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_tweet_idtweet_url(self):
        response = self.client.delete('/api/tweets/1/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_post_retweet_idtweet_url(self):
        response = self.client.post('/api/retweet/1/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)