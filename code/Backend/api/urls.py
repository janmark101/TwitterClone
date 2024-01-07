from django.urls import path, include
from .views import OnlyTweetView, FullTweetView, UsersTweetsView,  TweetsFromFollowedView, AllTweetsLikedCommentedFromFollowed ,\
    UserRetweetedTweetsView,TweetObjectView, RetweetView

urlpatterns = [
    path('comments/',include('apiComments.urls')),
    path('likes/',include('apiLikes.urls')),
    path('tweets/',OnlyTweetView.as_view(),name='tweets'),
    path('fullapi/',FullTweetView.as_view(),name='fullapi'),
    path('userstweets/',UsersTweetsView.as_view(),name='userstweets'),
    path('tweetsfromfollowed/',TweetsFromFollowedView.as_view(),name='tweetsfromfollowed'),
    path('tweetslinkedwithfollowed/',AllTweetsLikedCommentedFromFollowed.as_view()),
    path('userretweetedtweets/',UserRetweetedTweetsView.as_view()),
    path('tweet/<int:pk>/',TweetObjectView.as_view()),
    path('retweet/<int:pk>/',RetweetView.as_view())
]