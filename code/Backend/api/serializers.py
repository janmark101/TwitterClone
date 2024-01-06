from rest_framework import serializers
from .models import Comment,Like,Tweet

        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields = '__all__'
        read_only_fields = ['user']
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']
        
    

        
class TweetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ['user']
        
        