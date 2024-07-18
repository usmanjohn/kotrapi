from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=password
        )
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user