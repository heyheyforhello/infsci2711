from django import forms
from .models import Salesperson, Store#, Region

class SalespersonForm(forms.ModelForm):
    class Meta:
        model = Salesperson
        exclude = ['store_id']

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ['aid']

# class RegionForm(forms.ModelForm):
#     class Meta:
#         model = Region
#         exclude = []
