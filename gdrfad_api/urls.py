from django.urls import re_path, path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("gdrfad/dashboard", views.dashboard_view, name="dashboard_view"),
    path("gdrfad/increment-robot-options", views.increment_robot_options_view, name="increment_robot_options_view"),
]

urlpatterns = format_suffix_patterns(urlpatterns)