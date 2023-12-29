from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('id','username','email','password','password_confirm')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_username(self,value):
        if len(value) < 5 :
            raise serializers.ValidationError('Username must be at least 5 characters long!')
        if value.isdigit():
            raise serializers.ValidationError("Username cannot consist of only digits.") 
        return value
        
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'error': 'Passwords must match!'})
        return data

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user