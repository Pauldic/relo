from django import forms
from core.models import RetailerAccount, StoreAccount


class RetailerAccountForm(forms.ModelForm):
    class Meta:
        model = RetailerAccount
        fields = '__all__'


class StoreAccountForm(forms.ModelForm):

    class Meta:
        model = StoreAccount
        fields = '__all__'
