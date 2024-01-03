from .models import Comment,Tweet,Like
from .serializers import TweetSerializer
from rest_framework.views import APIViews

class TweetView(APIView):
    
