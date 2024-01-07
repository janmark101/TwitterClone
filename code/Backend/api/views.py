from .models import Comment,Tweet,Like
from .serializers import TweetSerializer, LikeSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .permissions import IsObjectOwner

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
class TweetsFromFollowedView(APIView):
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

# all tweets linked to people which logged user follows
class AllTweetsLikedCommentedFromFollowed(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        user_followed_list = request.user.following.all()
        created_tweets  = Tweet.objects.filter(user__in=user_followed_list)
        commented_tweets = Tweet.objects.filter(
            Q(comment__user__in=user_followed_list)  
        )
        retweeted = Tweet.objects.filter(retweets__in=user_followed_list)
        tweets = (commented_tweets | created_tweets | retweeted).distinct()
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
    
#list oof tweets which user retweeted
class UserRetweetedTweetsView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweets = Tweet.objects.filter(retweets=request.user)
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
    
# single tweet object and creating tweet
class TweetObjectView(APIView):
    permission_classes=[IsAuthenticated,IsObjectOwner]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request,pk):
        tweet = get_object_or_404(Tweet,pk=pk)
        likes = Like.objects.filter(tweet=tweet)
        comments = Comment.objects.filter(tweet=tweet)
        tweet_serializer = TweetSerializer(tweet,many=False).data
        likes_serializer = LikeSerializer(likes,many=True).data
        comments_serializer = CommentSerializer(comments,many=True).data
        data = [{
            'tweet' : tweet_serializer,
            'likes' : likes_serializer,
            'comments' : comments_serializer,
            'likes_count' : len(likes_serializer),
            'comments_count' : len(comments_serializer)
        }]
        return Response(data,status=status.HTTP_200_OK)
    
    def delete(self,request,pk):
        tweet = get_object_or_404(Tweet,pk=pk)
        self.check_object_permissions(request, tweet)
        tweet.delete()
        return Response({'message': 'Succesfully deleted.'},status=status.HTTP_200_OK)
    
#view to retweet tweets
class RetweetView(APIView):
    permission_classes=[IsAuthenticated,IsObjectOwner]
    authentication_classes=[TokenAuthentication]
    
    def post(self,request,pk):
        tweet = get_object_or_404(Tweet,pk=pk)
        tweet.retweets.add(request.user)
        return Response({'message' : 'Tweet retweeted.'},status=status.HTTP_200_OK)