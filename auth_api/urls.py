from django.urls import re_path, path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('signup/', views.user_create_view, name='user_create_view'),
    path('custom-signup/', views.custom_user_viewset_view, name='custom_user_viewset_view'),
    path('login/', views.custom_token_create_view, name='custom_token_create_view'),
    path('logout/', views.custom_token_destroy_view, name='custom_token_destroy_view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)