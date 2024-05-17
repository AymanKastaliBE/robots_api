from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.home_page_view, name="home_page_view"),
    path('profile/', views.user_profile_view, name="user_profile_view"),
]
