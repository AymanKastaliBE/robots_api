from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from rest_framework import views as rest_views
from django import views as django_views
from django.utils.decorators import method_decorator
from auth_api import decorators as auth_decorators
from . import models, forms, filters
from django.views import generic

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

@method_decorator(auth_decorators.allow_user_in_groups(groups=['Staff']), name='dispatch')
class BillListView(generic.ListView):
    model = models.Bill
    template_name = 'ata_api/bills.html'
    context_object_name = 'bills'
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('issued_at')
        self.bill_filter = filters.BillFilter(self.request.GET, queryset=queryset)
        return self.bill_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bill_filter = filters.BillFilter(data=self.request.GET)
        context['bill_filter'] = bill_filter
        context['balance'] = models.Balance.objects.first()
        return context
    
bill_list_view = BillListView.as_view()
    

class BillDetailView(generic.DetailView):
    model = models.Bill
    template_name = 'ata_api/bill_detail.html'
    queryset = models.Bill.objects.all()
    
bill_detail_view = BillDetailView.as_view()


class BillCreateView(generic.edit.CreateView):
    model = models.Bill
    form_class = forms.BillForm
    template_name = 'ata_api/bill_create.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ata_api:bill_detail_view', kwargs={'pk': self.object.pk})

bill_create_view = BillCreateView.as_view()


class BillUpdateView(generic.edit.UpdateView):
    model = models.Bill
    form_class = forms.BillForm
    template_name = 'ata_api/bill_update.html'
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('ata_api:bill_detail_view', kwargs={'pk': self.object.pk})

bill_update_view = BillUpdateView.as_view()


class BillDeleteView(generic.edit.DeleteView):
    model = models.Bill
    template_name = 'ata_api/bill_delete.html'
    success_url = reverse_lazy('ata_api:bill_list_view')

bill_delete_view = BillDeleteView.as_view()