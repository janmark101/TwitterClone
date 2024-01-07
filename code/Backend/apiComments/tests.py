from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from api.models import Tweet,Comment
from Authentication.models import User


class OnlyCommentsView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        self.tweet = Tweet.objects.create(content='test tweet',user=self.user)
        
    def test_get_all_comments(self):
        response = self.client.get('/api/comments/allcomments/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_create_comment(self):
        data = {'text':'test comment','tweet' : self.tweet.id}
        response = self.client.post('/api/comments/allcomments/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_creating_comment_to_not_existing_tweet(self):
        data = {'text':'test comment','tweet' : '404'}
        response = self.client.post('/api/comments/allcomments/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
class UserCoommentedTweetsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_all_commented_tweets(self):
        response = self.client.get('/api/comments/usercommentedtweets/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
class CommentedTweetsFromFollowedTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}') 
        
    def test_get_all_commented_tweets_from_followed(self):
        response = self.client.get('/api/comments/commentedtweetsfromfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
class DeleteCommentTesst(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',password='123',email='test@gmail.com')
        token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.tweet = Tweet.objects.create(content='test tweet',user=self.user)
        self.comment = Comment.objects.create(text='test comment',user=self.user,tweet=self.tweet)
        
    def test_delete_comment(self):
        response = self.client.delete(f'/api/comments/delete/{self.comment.id}/',format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_delete_not_existing_comment(self):
        response = self.client.delete('/api/comments/delete/404/',format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_delete_not_yours_comment(self):
        user_temp = User.objects.create(username='testtemp',password='123',email='testtemp@gmail.com')
        comment_temp = Comment.objects.create(text='test comment',user=user_temp,tweet=self.tweet)
        response = self.client.delete(f'/api/comments/delete/{comment_temp.id}/',format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
class TestNoPermissionURLS(APITestCase):
    def setUp(self):
        self.client = self.client_class() 
        
    def test_get_allcomments_url(self):
        response = self.client.get('/api/comments/allcomments/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_post_allcomments_url(self):
        response = self.client.post('/api/comments/allcomments/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_usercommented_url(self):
        response = self.client.get('/api/comments/usercommentedtweets/',None,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_commentedtweetsfromfollowed_url(self):
        response = self.client.get('/api/comments/commentedtweetsfromfollowed/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_idcomment_url(self):
        response = self.client.delete(f'/api/comments/delete/1/',format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
