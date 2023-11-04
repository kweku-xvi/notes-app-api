from rest_framework import serializers
from .models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)

    class Meta:
        model = UserModel
        fields = ['id','first_name', 'last_name','email', 'username', 'password', 'token']

        read_only_fields = ['token']