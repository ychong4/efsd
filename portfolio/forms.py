from django import forms
from .models import Customer, Stock, Investment, MutualFund

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_number', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone')


class StockForm(forms.ModelForm):
   class Meta:
       model = Stock
       fields = ('customer', 'symbol', 'name', 'shares', 'purchase_price', 'purchase_date',)

class InvestForm(forms.ModelForm):
   class Meta:
       model = Investment
       fields = ('customer', 'category', 'description', 'acquired_value', 'acquired_date', 'recent_value', 'recent_date')

class MutualFundForm(forms.ModelForm):
   class Meta:
       model = MutualFund
       fields = ('customer', 'fund', 'risk_level', 'acquired_value', 'acquired_date', 'recent_value', 'recent_date')

class EmailForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email']