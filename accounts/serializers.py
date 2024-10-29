from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import User, Dispatcher, Driver

User = get_user_model()

class UserCreateSerializerr(UserCreateSerializer):
    company = serializers.CharField(required=False, allow_null=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "company", "password", "is_dispatcher", "is_driver")
