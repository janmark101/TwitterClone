from django.urls import path
from .views import OnlyLikesView, LikedTweetsForUserView, LikeTweetView,LikedTweetsFromFollowedView

urlpatterns = [
    path('alllikes/',OnlyLikesView.as_view(),name='likes'),
    path('userlikedtweets/',LikedTweetsForUserView.as_view(),name='userlikedtweets'),
    path('liketweet/',LikeTweetView.as_view(),name='liketweets'),
    path('likedtweetsfromfollowed/',LikedTweetsFromFollowedView.as_view())
]
