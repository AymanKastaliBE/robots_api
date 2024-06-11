from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page_view, name="home_page_view"),
    path('profile/', views.user_profile_view, name="user_profile_view"),
    path('bills/', views.bill_list_view, name="bill_list_view"),
    path('bills/<uuid:pk>/', views.bill_detail_view, name="bill_detail_view"),
    path('bills/create/', views.bill_create_view, name="bill_create_view"),
    path('bills/<uuid:pk>/update/', views.bill_update_view, name='bill_update_view'),
    path('bills/<uuid:pk>/delete/', views.bill_delete_view, name='bill_delete_view'),
]
