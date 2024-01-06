from django.shortcuts import render
from api.models import Comment,Tweet,Like
from api.serializers import TweetSerializer, LikeSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
# Create your views here.


#all likes 
class OnlyLikesView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweets = Like.objects.all()
        serializer = LikeSerializer(tweets,many=True)
        return Response(serializer.data)
    
    
 # liked tweets
class LikedTweetsForUserView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweets = Tweet.objects.filter(like__user=request.user)
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
    
 # function to like or unlike tweets   
class LikeTweetView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def post(self,request):
        serializer = LikeSerializer(data=request.data)
        
        if serializer.is_valid():
            tweet = serializer.validated_data['tweet']
            like,created = Like.objects.get_or_create(tweet=tweet,user=request.user)
            if not created:
                like.delete()
                return Response({'message' : 'Unliked tweet succesfully!'},status=status.HTTP_201_CREATED)
            else:
                return Response({'message' : 'Liked tweet succesfully!'},status=status.HTTP_201_CREATED)
        return Response({'error' : 'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)
    
    
class LikedTweetsFromFollowedView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        user_following_list = request.user.following.all()
        tweets = Tweet.objects.filter(Q(like__user__in=user_following_list))
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