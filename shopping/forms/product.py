from django import forms
from shopping.models import Product, Coupon, Banner
from django.forms import ModelForm
import re
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['name', 'normalprice','description','image','stock','category']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'normalprice' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control','rows': 4}),         
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class':'form-control'}),

        }


# class CouponForm(forms.ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['coupon_code', 'is_active', 'discount_price', 'minimum_amount', 'user','description']
#         labels = {
#             'coupon_code': 'Coupon Code',
#             'is_active': 'Is Active',
#             'discount_price': 'Discount Price',
#             'minimum_amount': 'Minimum Amount',
#             'description': 'description',
#             'user': 'User',
#         }
#         widgets = {
#             'coupon_code': forms.TextInput(attrs={'class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
#             'minimum_amount': forms.NumberInput(attrs={'class': 'form-control'}),
#             'description': forms.TextInput(attrs={'class': 'form-control'}),
#             'user': forms.Select(attrs={'class': 'form-control'}),
#         }


