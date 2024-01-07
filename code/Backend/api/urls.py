from django.urls import path, include
from .views import OnlyTweetView, FullTweetView, UsersTweetsView,  TweetsFroUserFromFollowedView, AllTweetsLikedCommentedFromFollowed ,\
    UserRetweetedTweetsView,TweetObjectView, RetweetsView

urlpatterns = [
    path('comments/',include('apiComments.urls')),
    path('likes/',include('apiLikes.urls')),
    path('tweets/',OnlyTweetView.as_view(),name='tweets'),
    path('fullapi/',FullTweetView.as_view(),name='fullapi'),
    path('userstweets/',UsersTweetsView.as_view(),name='userstweets'),
    path('tweetsfromfollowed/',TweetsFroUserFromFollowedView.as_view(),name='tweetsfromfollowed'),
    path('tweetslinkedwithfollowed/',AllTweetsLikedCommentedFromFollowed.as_view()),
    path('userretweetedtweets/',UserRetweetedTweetsView.as_view()),
    path('tweet/<int:pk>/',TweetObjectView.as_view()),
    path('retweet/<int:pk>/',RetweetsView.as_view())
]