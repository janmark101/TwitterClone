from django.db import models
from Authentication.models import User

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    content = models.TextField(max_length=500,null=False,blank=False)
    retweets = models.ManyToManyField(User, related_name='retweeted_tweets', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user}'s tweet : {self.id}"
    
class Like(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='liked_tweet', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_liker', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} liked : {self.tweet}"

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=250,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"comment to : {self.tweet}"