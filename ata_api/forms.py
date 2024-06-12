from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, Row, Column


class BillForm(forms.ModelForm):
    class Meta:
        model = models.Bill
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['issued_at'].widget = forms.DateInput(attrs={'type': 'date'})
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('staff', css_class='col-md-4'),
                    Column('issued_at', css_class='col-md-4'),
                    Column('supplier_name', css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column('invoice_number', css_class='col-md-4'),
                    Column('transaction_number', css_class='col-md-4'),
                    Column('vat', css_class='col-md-4'),
                    css_class='row'
                ),
                 Row(
                    Column('amount', css_class='col-md-4'),
                    Column('remark', css_class='col-md-4'),
                    Column('scanned_pdf', css_class='col-md-4'),
                    css_class='row'
                ),
                Submit('submit', 'Save', css_class='btn btn-primary fw-bold'),
            )
        )
