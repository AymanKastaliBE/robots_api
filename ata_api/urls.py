from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page_view, name="home_page_view"),
    path('profile/', views.user_profile_view, name="user_profile_view"),
    path('bills/', views.bills_view, name="bills_view"),
    path('bills/<uuid:pk>/', views.bills_view, name="bills_view"),
]
