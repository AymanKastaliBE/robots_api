from django.urls import re_path, path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("gdrfad/dashboard", views.dashboard_view, name="dashboard_view"),
]

urlpatterns = format_suffix_patterns(urlpatterns)