from django.urls import path
from .views import OnlyLikesView, UserLikedTweetsView, LikeTweetView,LikedTweetsFromFollowedView

urlpatterns = [
    path('alllikes/',OnlyLikesView.as_view(),name='likes'),
    path('userlikedtweets/',UserLikedTweetsView.as_view(),name='userlikedtweets'),
    path('liketweet/',LikeTweetView.as_view(),name='liketweets'),
    path('likedtweetsfromfollowed/',LikedTweetsFromFollowedView.as_view())
]
