from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import  status, views
from djoser.views import TokenCreateView
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .decorators import protect_login_page_from_logged_in_users
from django.utils.decorators import method_decorator
from djoser.conf import settings as djoser_settings
from djoser import utils
from djoser import views as d
from rest_framework.permissions import AllowAny
from django.conf import settings as django_settings
from djoser.views import UserViewSet
from djoser.serializers import UserCreateSerializer
from . import serializers as auth_serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.sessions.models import Session
from django.utils import timezone


User = get_user_model()


class CustomSignupView(views.APIView):
    template_name = 'auth_api/signup.html'
    permission_classes = [AllowAny]

    def get(self, request):
        SIGNUP_URL_POST = django_settings.SIGNUP_URL_POST
        LOGIN_URL_GET = django_settings.LOGIN_URL_GET
        context = {
            'SIGNUP_URL_POST': SIGNUP_URL_POST,
            'LOGIN_URL_GET': LOGIN_URL_GET,
        }
        return render(request, template_name=self.template_name, context=context)

custom_signup_view = CustomSignupView.as_view()


class CustomUserRegistrationView(UserViewSet):
    serializer_class = djoser_settings.SERIALIZERS.user_create
    
    def perform_create(self, serializer):
        user = serializer.save()
        return redirect(reverse_lazy(django_settings.LOGIN_URL_GET))
    
custom_user_registration_view = CustomUserRegistrationView.as_view({'post': 'create'})



class CustomLoginView(views.APIView):
    template_name = 'auth_api/login.html'
    permission_classes = [AllowAny]

    def get(self, request):
        LOGIN_URL_POST = django_settings.LOGIN_URL_POST
        USER_PROFILE_URL = django_settings.USER_PROFILE_URL
        context = {
            'LOGIN_URL_POST': LOGIN_URL_POST,
            'USER_PROFILE_URL': USER_PROFILE_URL,
        }
        return render(request, template_name=self.template_name, context=context)

custom_login_view = CustomLoginView.as_view()


class CustomJWTTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # username = request.data.get('username', 'User')
        response = super().post(request, *args, **kwargs)
        # Obtain access token and refresh token from the response data
        access_token = response.data['access']
        refresh_token = response.data['refresh']

        # Set expiration time for the cookies
        access_token_expiration = datetime.now() + django_settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_expiration = datetime.now() + django_settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        # Create HTTP-only cookies for access and refresh tokens
        response.set_cookie('access_token', access_token, expires=access_token_expiration, httponly=True)
        response.set_cookie('refresh_token', str(refresh_token), expires=refresh_token_expiration, httponly=True)
        # response.set_cookie('username', username, expires=access_token_expiration)

        response.data['custom_field'] = 'Custom value'

        return response

custom_jwt_token_create_view = CustomJWTTokenObtainPairView.as_view()


class CustomTokenDestroyView(views.APIView):
    template_name = 'auth_api/logout.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request):
        try:
            # Retrieve the refresh token from the cookies
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Blacklist the refresh token
                refresh_token_obj = RefreshToken(refresh_token)
                refresh_token_obj.blacklist()
            except Exception as e:
                return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            # Create response and delete cookies
            response = Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

custom_token_destroy_view = CustomTokenDestroyView.as_view()

# class CustomTokenDestroyView(views.APIView):
#     template_name = 'auth_api/logout.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, template_name=self.template_name)

#     def post(self, request):
#         try:
#             print("request: ", request.COOKIES)
#             response = Response({'message': 'Logged out successfully'}, status=status.HTTP_204_NO_CONTENT)
#             response.delete_cookie('access_token')
#             response.delete_cookie('refresh_token')
#             # response.delete_cookie('username')
#             return response

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# custom_token_destroy_view = CustomTokenDestroyView.as_view()