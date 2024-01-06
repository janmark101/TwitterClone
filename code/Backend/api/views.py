from .models import Comment,Tweet,Like
from .serializers import TweetSerializer, LikeSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

#all tweets and creating tweet
class OnlyTweetView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweet = Tweet.objects.all()
        serializer = TweetSerializer(tweet,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = TweetSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            Tweet.objects.create(content=serializer.validated_data['content'],user=user)
            return Response({'message' : 'Tweet created succesfully!'},status=status.HTTP_201_CREATED)
        return Response({'error' : 'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)
   

 # tweets with likes and comments   
class FullTweetView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        tweets = Tweet.objects.all()
        tweet_data = []

        for tweet in tweets:
            tweet_serializer = TweetSerializer(tweet).data
            like_serializer = LikeSerializer(Like.objects.filter(tweet=tweet), many=True).data
            comment_serializer = CommentSerializer(Comment.objects.filter(tweet=tweet), many=True).data

            tweet_data.append({
                'tweet': tweet_serializer,
                'likes': like_serializer,
                'comments': comment_serializer,
                'likes_count' : len(like_serializer),
                'comments_count' : len(comment_serializer)
            })

        return Response(tweet_data, status=status.HTTP_200_OK)
        
        
# user's tweets with likes and comments
class UsersTweetsView(APIView):
    def get(self,request):
        tweets = Tweet.objects.filter(user=request.user)
        tweet_data = []

        for tweet in tweets:
            tweet_serializer = TweetSerializer(tweet).data
            like_serializer = LikeSerializer(Like.objects.filter(tweet=tweet), many=True).data
            comment_serializer = CommentSerializer(Comment.objects.filter(tweet=tweet), many=True).data

            tweet_data.append({
                'tweet': tweet_serializer,
                'likes': like_serializer,
                'comments': comment_serializer,
                'likes_count' : len(like_serializer),
                'comments_count' : len(comment_serializer)
            })

        return Response(tweet_data, status=status.HTTP_200_OK)
     
 
#tweets from followed users
class TweetsFroUserFromFollowedView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        user_followed_list = request.user.following.all()
        tweets = Tweet.objects.filter(user__in=user_followed_list)
        tweet_data = []
        for tweet in tweets:
            tweet_serializer = TweetSerializer(tweet).data
            like_serializer = LikeSerializer(Like.objects.filter(tweet=tweet), many=True).data
            comment_serializer = CommentSerializer(Comment.objects.filter(tweet=tweet), many=True).data

            tweet_data.append({
                'tweet': tweet_serializer,
                'likes': like_serializer,
                'comments': comment_serializer,
                'likes_count' : len(like_serializer),
                'comments_count' : len(comment_serializer)
            })

        return Response(tweet_data, status=status.HTTP_200_OK)

class AllTweetsLikedCommentedFromFollowed(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        user_followed_list = request.user.following.all()
        created_tweets  = Tweet.objects.filter(user__in=user_followed_list)
        commented_tweets = Tweet.objects.filter(
            Q(comment__user__in=user_followed_list)  
        )
        tweets = (commented_tweets | created_tweets).distinct()
        tweet_data = []
        for tweet in tweets:
            tweet_serializer = TweetSerializer(tweet).data
            like_serializer = LikeSerializer(Like.objects.filter(tweet=tweet), many=True).data
            comment_serializer = CommentSerializer(Comment.objects.filter(tweet=tweet), many=True).data

            tweet_data.append({
                'tweet': tweet_serializer,
                'likes': like_serializer,
                'comments': comment_serializer,
                'likes_count' : len(like_serializer),
                'comments_count' : len(comment_serializer)
            })

        return Response(tweet_data, status=status.HTTP_200_OK)
    