from rest_framework import serializers
from .models import AndroidApp, UserAppTask
from django.contrib.auth import get_user_model

User = get_user_model()

class AndroidAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = AndroidApp
        fields = [
            'id', 'name', 'description', 'package_name', 
            'points_value', 'category', 'app_icon', 
            'playstore_link', 'is_active'
        ]
        read_only_fields = ['id']

class UserAppTaskSerializer(serializers.ModelSerializer):
    app = AndroidAppSerializer(read_only=True)
    app_id = serializers.PrimaryKeyRelatedField(
        queryset=AndroidApp.objects.all(), 
        source='app', 
        write_only=True
    )

    class Meta:
        model = UserAppTask
        fields = [
            'id', 'app', 'app_id', 'status', 
            'screenshot', 'points_earned', 
            'submitted_at', 'approved_at'
        ]
        read_only_fields = [
            'id', 'points_earned', 
            'submitted_at', 'approved_at'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'is_staff', 'is_active', 'profile', 'date_created','total_points'
        ]
        read_only_fields = ['id', 'date_created']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data.get('password', None)
        )
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile = validated_data.get('profile', instance.profile)
        instance.save()
        return instance
class UserAppTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAppTask
        fields = ['app', 'screenshot']