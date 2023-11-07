import os
from .serializers import RegisterUserSerializer, LoginUserSerializer, UserSerializer
from .models import User
from .utils import send_password_reset_email
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import response, status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import GenericAPIView

load_dotenv()


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
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return response.Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
def password_reset_view(request):
    if request.method == 'POST':
        email = request.data.get('email')

        if not email:
            return response.Response(
                {
                    'sucess':False,
                    'message':'Email is required'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request).domain
            relative_link = reverse('password_reset_confirm_view')
            absolute_url = f'http://{current_site}{relative_link}?uid={uid}&token={token}'
            link = str(absolute_url)
            send_password_reset_email(link=link, email=email, username=user.username)
            return response.Response(
                {
                    'sucess':True,
                    'message': 'Password Reset Email Sent',
                }, status=status.HTTP_200_OK
            )
        except User.DoesNotExist as e:
            return response.Response(
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return response.Response(
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['PATCH'])
@authentication_classes([])
def password_reset_confirm_view(request):
    if request.method == 'PATCH':
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not uid or not token or not password:
            return response.Response(
                {
                    'sucess':False,
                    'message':'All fields are required'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_id = urlsafe_base64_encode(uid)
            user = User.objects.get(id=user_id)
            if not default_token_generator.check_token(user, token):
                return response.Response(
                    {
                        'success':False,
                        'message':'Invalid token'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
                user.set_password(password)
                user.save()
                return response.Response(
                    {
                        'success':True,
                        'message':'Your password has been reset',
                    }, status=status.HTTP_200_OK
                )
        except User.DoesNotExist as e:
            return response.Response(
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return response.Response(
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )