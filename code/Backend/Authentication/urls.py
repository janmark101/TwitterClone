from django.urls import path
from .views import Login,Logout,Register,VerifyAccount, UsersListView, UserObjectView,FollowersFollowingForUser, \
    ChangeCustomNameView, FollowUserView, ChangePasswordView

urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('register/',Register.as_view(),name='register'),
    path('verifyacc/',VerifyAccount.as_view(),name='register'),
    path('users/',UsersListView.as_view()),
    path('users/<int:pk>/',UserObjectView.as_view()),
    path('followersfollowinguser/',FollowersFollowingForUser.as_view()),
    path('changecustomname/',ChangeCustomNameView.as_view()),
    path('changepassword/',ChangePasswordView.as_view()),
    path('followuser/<int:pk>/',FollowUserView.as_view())
]
