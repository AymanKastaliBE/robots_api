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


User = get_user_model()

class UserCreateView(views.APIView):
    template_name = 'auth_api/signup.html'
    permission_classes = [AllowAny]
    def get(self, request):
        SIGNUP_URL_POST = django_settings.SIGNUP_URL_POST
        LOGIN_URL = django_settings.LOGIN_URL
        context = {
            'SIGNUP_URL_POST': SIGNUP_URL_POST,
            'LOGIN_URL': LOGIN_URL,
        }
        return render(request, template_name=self.template_name, context=context)
       
user_create_view = UserCreateView.as_view()



class CustomUserViewSet(UserViewSet):
    serializer_class = djoser_settings.SERIALIZERS.user_create
    
    def perform_create(self, serializer):
        user = serializer.save()
        return redirect(reverse_lazy(django_settings.LOGIN_URL))
    
custom_user_viewset_view = CustomUserViewSet.as_view({'post': 'create'})
 

class CustomTokenCreateView(TokenCreateView):
    template_name = 'auth_api/login.html'
    
    @method_decorator(protect_login_page_from_logged_in_users, name='dispatch')
    def get(self, request, *args, **kwargs):
        LOGIN_URL = django_settings.LOGIN_URL
        USER_PROFILE_URL = django_settings.USER_PROFILE_URL
        context = {
            'LOGIN_URL': LOGIN_URL,
            'USER_PROFILE_URL': USER_PROFILE_URL,
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({'auth_token': token.key}, status=status.HTTP_200_OK)
            response.set_cookie('auth_token', token.key, httponly=True)
            
            login(request, user)
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
custom_token_create_view = CustomTokenCreateView.as_view()


class CustomTokenDestroyView(views.APIView):
    permission_classes = djoser_settings.PERMISSIONS.token_destroy
    template_name = 'auth_api/logout.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request):
        if 'auth_token' in request.COOKIES:
            auth_token = request.COOKIES.get('auth_token')

            try:
                token = Token.objects.get(key=auth_token)
                token.delete()
            except Token.DoesNotExist:
                pass

            utils.logout_user(request)
            response = Response({'message': 'logged out successfully'}, status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie('auth_token')
            
            login_url = reverse_lazy('login')
            response['Location'] = login_url
            logout(request)
            return response

        return Response({'error': 'No auth token found in cookies'}, status=status.HTTP_400_BAD_REQUEST)

custom_token_destroy_view = CustomTokenDestroyView.as_view()