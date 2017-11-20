from django import forms

from product.models import BrandAccount, Brand


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandAccountForm(forms.ModelForm):
    class Meta:
        model = BrandAccount
        fields = ('brand', 'title', 'website', 'email', 'name', 'file')


