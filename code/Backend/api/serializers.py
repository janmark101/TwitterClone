from rest_framework import serializers
from .models import Comment,Like,Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'
        
        