from django.urls import path
from .views import CommentedTweetsFroUserView, OnlyCommentView,ComentedTweetsFromFollowedView,DeleteCommentView

urlpatterns = [
    path('allcomments/',OnlyCommentView.as_view(),name='comments'),
    path('usercommentedtweets/',CommentedTweetsFroUserView.as_view(),name='usercommentedtweets'),
    path('commentedtweetsfromfollowed/',ComentedTweetsFromFollowedView.as_view()),
    path('<int:pk>/',DeleteCommentView.as_view())
]