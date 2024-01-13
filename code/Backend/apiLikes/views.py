from api.models import Comment,Tweet,Like
from api.serializers import TweetSerializer, LikeSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from api.views import get_tweets_data


#all likes 
class OnlyLikesView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweets = Like.objects.all()
        serializer = LikeSerializer(tweets,many=True)
        return Response(serializer.data)
    
    
 # liked tweets
class UserLikedTweetsView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweets = Tweet.objects.filter(like__user=request.user)
        tweet_data = get_tweets_data(tweets)
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
                return Response({'message' : 'Unliked tweet succesfully!'},status=status.HTTP_200_OK)
            else:
                return Response({'message' : 'Liked tweet succesfully!'},status=status.HTTP_201_CREATED)
        return Response({'error' : 'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)
    
    
class LikedTweetsFromFollowedView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        user_following_list = request.user.following.all()
        tweets = Tweet.objects.filter(Q(like__user__in=user_following_list))
        tweet_data = get_tweets_data(tweets)
        return Response(tweet_data, status=status.HTTP_200_OK)