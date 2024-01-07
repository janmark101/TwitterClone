from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from api.models import Tweet,Like
from Authentication.models import User

class AllLikesTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        
    def test_get_all_likes(self):
        response = self.client.get('/api/likes/alllikes/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
class UserLikedTweetsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        
    def test_get_user_liked_tweets(self):
        response = self.client.get('/api/likes/userlikedtweets/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
       
        
class LikeTweetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.tweet = Tweet.objects.create(content='test tweet',user=self.user)
        
    def test_like_tweet(self):
        data = { 'tweet' : self.tweet.id}
        response = self.client.post('/api/likes/liketweet/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    def test_unlike_tweet(self):
        like = Like.objects.create(tweet=self.tweet,user=self.user)
        data = { 'tweet' : self.tweet.id}
        response = self.client.post('/api/likes/liketweet/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_like_tweet_invalid_tweetid(self):
        data = { 'tweet' : 404}
        response = self.client.post('/api/likes/liketweet/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        
class LikedTweetsFromFollowedTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.tweet = Tweet.objects.create(content='test tweet',user=self.user)
        
    def test_get_liked_tweets_from_followed(self):
        response = self.client.get('/api/likes/likedtweetsfromfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class TestNoPermissionURLS(APITestCase):
    def setUp(self):
        self.client = self.client_class() 
        
    def test_get_alllikes_url(self):
        response = self.client.get('/api/likes/alllikes/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_userlikedtweets_url(self):
        response = self.client.get('/api/likes/userlikedtweets/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_post_liketweet_url(self):
        response = self.client.post('/api/likes/liketweet/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_likedtweetsfromfollowed_url(self):
        response = self.client.get('/api/likes/likedtweetsfromfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
