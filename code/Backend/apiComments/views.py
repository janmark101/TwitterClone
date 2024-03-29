from django.shortcuts import get_object_or_404
from api.models import Comment,Tweet,Like
from api.serializers import TweetSerializer, LikeSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from api.permissions import IsObjectOwner
from api.views import get_tweets_data
# Create your views here.




#all comments and creating a comment
class OnlyCommentsView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweets = Comment.objects.all()
        serializer = CommentSerializer(tweets,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CommentSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            Comment.objects.create(text=serializer.validated_data['text'],tweet=serializer.validated_data['tweet'],user=user)
            return Response({'message' : 'Comment created succesfully!'},status=status.HTTP_201_CREATED)
        return Response({'error' : 'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)
    
#all commented tweets by user
class UserCommentedTweetsView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        tweets = Tweet.objects.filter(comment__user=request.user)  
        tweet_data = get_tweets_data(tweets)
        return Response(tweet_data, status=status.HTTP_200_OK)
    
# all tweets commented by userss which logged user follow
class ComentedTweetsFromFollowedView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        user_followed_list = request.user.following.all()
        tweets = Tweet.objects.filter(Q(comment__user__in=user_followed_list)) 
        tweet_data = get_tweets_data(tweets)
        return Response(tweet_data, status=status.HTTP_200_OK)
    
    
class DeleteCommentView(APIView):
    permission_classes=[IsAuthenticated,IsObjectOwner]
    authentication_classes=[TokenAuthentication]
    
    def delete(self,request,pk):
        comment = get_object_or_404(Comment,pk=pk)
        self.check_object_permissions(request,comment)
        comment.delete()
        return Response({'message': 'Succesfully deleted.'},status=status.HTTP_200_OK)