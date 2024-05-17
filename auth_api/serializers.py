from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers


class CustomUserCreateSerializer(DjoserUserCreateSerializer):
    password_retype = serializers.CharField(write_only=True)

    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ('username', 'password', 'password_retype')