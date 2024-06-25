from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from rest_framework import views as rest_views
from django import views as django_views
from django.utils.decorators import method_decorator
from auth_api import decorators as auth_decorators
from . import models, forms, filters
from django.views import generic, View
import pandas as pd
from django.http import HttpResponse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin


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
    template_name = 'ata_api/bills/bills.html'
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
    template_name = 'ata_api/bills/bill_detail.html'
    queryset = models.Bill.objects.all()
    
bill_detail_view = BillDetailView.as_view()


class BillCreateView(generic.edit.CreateView):
    model = models.Bill
    form_class = forms.BillForm
    template_name = 'ata_api/bills/bill_create.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ata_api:bill_detail_view', kwargs={'pk': self.object.pk})

bill_create_view = BillCreateView.as_view()


class BillUpdateView(generic.edit.UpdateView):
    model = models.Bill
    form_class = forms.BillForm
    template_name = 'ata_api/bills/bill_update.html'
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('ata_api:bill_detail_view', kwargs={'pk': self.object.pk})

bill_update_view = BillUpdateView.as_view()


class BillDeleteView(generic.edit.DeleteView):
    model = models.Bill
    template_name = 'ata_api/bills/bill_delete.html'
    success_url = reverse_lazy('ata_api:bill_list_view')

bill_delete_view = BillDeleteView.as_view()


@method_decorator(auth_decorators.allow_user_in_groups(groups=['Staff']), name='dispatch')
class BillExportToExcelView(View):
    
    def get(self, request, *args, **kwargs):
        # Get the queryset from the filter
        queryset = models.Bill.objects.order_by('issued_at')
        bill_filter = filters.BillFilter(request.GET, queryset=queryset)
        filtered_qs = bill_filter.qs
        
        # Convert the queryset to a DataFrame
        data = list(filtered_qs.values(
            'id', 'type', 'issued_at', 'staff__name', 'supplier_name',
            'invoice_number', 'transaction_number', 'amount', 'vat', 'remark'
        ))

        df = pd.DataFrame(data)
        
        df.rename(columns={
            'staff__name': 'staff name',
            'issued_at': 'date',
            'supplier_name': 'supplier name',
            'invoice_number': 'invoice number',
            'transaction_number': 'transaction number',
            'id': 'bill ID',
        }, inplace=True)
        
        df['Total Amount'] = df['vat'] + df['amount']
        
        df['Cash Received'] = df.apply(lambda row: row['amount'] if row['type'] == 'recharge' else None, axis=1)
        df['amount'] = df.apply(lambda row: '' if row['type'] == 'recharge' else row['amount'], axis=1)
        df['vat'] = df.apply(lambda row: '' if row['type'] == 'recharge' else row['vat'], axis=1)
        df['remark'] = df.apply(lambda row: '' if row['type'] == 'recharge' else row['remark'], axis=1)
        df['Total Amount'] = df.apply(lambda row: '' if row['type'] == 'recharge' else row['Total Amount'], axis=1)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=bills.xlsx'
        
        # Use pandas to write the DataFrame to an Excel file
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Bills')
        
        return response
    
bill_export_to_excel_view = BillExportToExcelView.as_view()


class DiabloView(django_views.View):
    template_name = 'ata_api/diablo/index.html'
    
    def get(self, request):
        return render(request, template_name=self.template_name)
    
diablo_view = DiabloView.as_view()