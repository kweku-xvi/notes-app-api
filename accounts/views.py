from django.shortcuts import render
from .serializers import RegisterUserSerializer, LoginUserSerializer, UserSerializer
from .models import UserModel
from  django.contrib.auth import authenticate
from rest_framework import response, status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import GenericAPIView


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def auth_user_api_view(request):
    user = request.data
    serializer = RegisterUserSerializer(user)
    return response.Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
def user_login(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    user = authenticate(username=email, password=password)

    if user:
        serializer = LoginUserSerializer(user)

        return response.Response(serializer.data, status=status.HTTP_200_OK)
    return response.Response({'message':'Invalid credentials. Try again.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([])
def get_all_users_view(request):
    users = UserModel.objects.all()

    serializer = UserSerializer(users, many=True)

    return response.Response(serializer.data, status=status.HTTP_200_OK)