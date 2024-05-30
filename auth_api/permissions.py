from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import BasePermission
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings

staff_group, _ = Group.objects.get_or_create(name='Staff')
gdrfad_group, _ = Group.objects.get_or_create(name='GDRFAD')

class StaffOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            login_url = settings.LOGIN_URL_GET
            return redirect(reverse(login_url))
        return request.user.groups.filter(name='Staff').exists()

class GDRFADOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            login_url = settings.LOGIN_URL_GET
            return redirect(reverse(login_url))
        return request.user.groups.filter(name='GDRFAD').exists()
