from django.urls import path, include
from django.conf import settings
from rest_framework import serializers
from apps.accounts.models import User, CHOICES
from rest_framework.exceptions import APIException
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'profile',
            'email',
            'first_name',
            'last_name',
            'password'
        ]

    def create(self, validated_data):
        user_dic = {}
        user_dic['profile'] = validated_data.get('profile')
        user_dic['email'] = validated_data.get('email')
        user_dic['first_name'] = validated_data.get('first_name')
        user_dic['last_name'] = validated_data.get('last_name')
        user_dic['password'] = make_password(validated_data.get('password'))
        instance = User.objects.create(**user_dic)
        return instance
