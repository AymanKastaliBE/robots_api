from django.shortcuts import render
from rest_framework import views as rest_views
from django import views as django_views
from django.utils.decorators import method_decorator
from auth_api import decorators as auth_decorators

class HomepageView(django_views.View):
    template_name = 'ata_api/homepage.html'
    
    def get(self, request):
        return render(request, template_name=self.template_name)
    
home_page_view = HomepageView.as_view()


class UserProfileView(django_views.View):
    template_name = 'ata_api/user_profile.html'
    
    def get(self, request):
        return render(request, template_name=self.template_name)
    
user_profile_view = UserProfileView.as_view()


class BillsView(django_views.View):
    template_name = 'ata_api/bills.html'
    
    @method_decorator(auth_decorators.allow_user_in_groups(groups=['Staff']))
    def get(self, request):
        return render(request, template_name=self.template_name)
    
bills_view = BillsView.as_view()