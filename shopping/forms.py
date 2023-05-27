from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Category, Address, Order,Coupon,Banner
from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Variant,Product,ProductVariant

class CreateUserForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=20)

    class Meta:
        model=User
        fields=['username', 'email', 'mobile_number', 'password1', 'password2']


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model=User
#         fields=['username','email','password1','password2']





class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and name.strip() == '':
            raise ValidationError('Name cannot be only spaces')
        if Category.objects.filter(name=name).exists():
            raise ValidationError('A category with this name already exists')
        return name

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name","housename", "locality", "phone", "city", "state", "zipcode"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'housename': forms.TextInput(attrs={'class': 'form-control'}),
            "locality": forms.TextInput(attrs={'class': 'form-control'}),
            "city": forms.TextInput(attrs={'class': 'form-control'}),
            "state": forms.Select(attrs={'class': 'form-control'}),
            "zipcode": forms.NumberInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),

        }
        labels={
            'name':'Name',
            'housename':'House no.',
            'locality':'Locality',
            'city':'City',
            'state':'State',
            'zipcode':'Zipcode',
            'phone':'Phone',
        }
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Phone number must be entered in the format: '9999999999'")
        return phone

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        if not re.match(r'^\d{6}$', str(zipcode)):
            raise ValidationError("Enter a valid zipcode.")
        return zipcode


        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordertype','status']
        widgets = {
            'ordertype' : forms.TextInput(attrs={'class':'form-control'}),
            'status' : forms.Select(attrs={'class':'form-control'}),
        }
        labels={
            'ordertype':'Order Type',
            'status':'Status',
        }



class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        if name.isspace():
            raise forms.ValidationError("Name cannot contain only spaces.")
        return name
        

class ProductVariantForm(ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['variant', 'price', 'stock']
ProductVariantFormSet = inlineformset_factory(Product, ProductVariant, form=ProductVariantForm, extra=1)
from .models import ProductVariant

class CartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        variant_choices = kwargs.pop('variant_choices')
        super().__init__(*args, **kwargs)
        self.fields['variant'] = forms.ChoiceField(choices=variant_choices)
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'is_active', 'discount_price', 'minimum_amount','description']
        labels = {
            'coupon_code': 'Coupon Code',
            'is_active': 'Is Active',
            'discount_price': 'Discount Price',
            'minimum_amount': 'Minimum Amount',
            'description': 'description',
            
        }
        widgets = {
            'coupon_code': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'minimum_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
           
        }
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['name', 'image']
        labels = {
            'name': 'Banner name',
            # 'image': 'Image',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class':'form-control'}),
        }