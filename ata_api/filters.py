import django_filters
from . import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, Row, Column

class BillFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(
        field_name='id',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Enter ID'}),
        label='',
    )
    issued_at_start = django_filters.DateFilter(
        field_name='issued_at',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='',
    )
    issued_at_end = django_filters.DateFilter(
        field_name='issued_at',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='',
    )
    staff_name = django_filters.CharFilter(
        field_name='staff__name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Enter Staff Name'}),
        label='',
    )
    invoice_number = django_filters.CharFilter(
        field_name='invoice_number',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Enter Invoice Number'}),
        label='',
    )
    transaction_number = django_filters.CharFilter(
        field_name='transaction_number',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Enter Transaction Number'}),
        label='',
    )

    class Meta:
        model = models.Bill
        fields = ['id', 'issued_at_start', 'issued_at_end', 'invoice_number', 'transaction_number', 'staff__name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = 'get'
        self.form.helper.layout = Layout(
            Div(
                Row(
                    Column('id', css_class='col'),
                    Column('staff_name', css_class='col'),
                    Column('invoice_number', css_class='col'),
                    Column('transaction_number', css_class='col'),
                    Column('issued_at_start', css_class='col'),
                    Column('issued_at_end', css_class='col'),
                    Column(
                        Submit('submit', 'Filter', css_class='btn btn-info fw-bold'),
                        css_class='col-auto'
                    ),
                    css_class='row g-4'
                ),
            )
        )
