from django.urls import path
from .views import UserCommentedTweetsView, OnlyCommentsView,ComentedTweetsFromFollowedView,DeleteCommentView

urlpatterns = [
    path('allcomments/',OnlyCommentsView.as_view(),name='comments'),
    path('usercommentedtweets/',UserCommentedTweetsView.as_view(),name='usercommentedtweets'),
    path('commentedtweetsfromfollowed/',ComentedTweetsFromFollowedView.as_view()),
    path('delete/<int:pk>/',DeleteCommentView.as_view())
]