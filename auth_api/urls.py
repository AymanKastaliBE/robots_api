from django.urls import re_path, path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('signup/', views.custom_signup_view, name='custom_signup_view'),
    path('custom-signup/', views.custom_user_registration_view, name='custom_user_registration_view'),
    path('login/', views.custom_login_view, name='custom_login_view'),
    path('custom-login/', views.custom_jwt_token_create_view, name='custom_jwt_token_create_view'),
    path('logout/', views.custom_token_destroy_view, name='custom_token_destroy_view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)