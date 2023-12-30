from django.urls import path
from .views import Login,Logout,Register,VerifyAccount

urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('register/',Register.as_view(),name='register'),
    path('verifyacc/',VerifyAccount.as_view(),name='register'),

]
