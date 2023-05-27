from django.shortcuts import render
from django.contrib.auth import*
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import HttpResponse
from django.core.cache import cache
from .models import Product,Address,Order,Image,Banner
from .models import MyAdmin,Coupon
from .forms import CreateUserForm,VariantForm,CouponForm,BannerForm

from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from .models import UserDetail, Product, Category
from .models import Category,Variant,Wallet
from .forms import CategoryForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CreateUserForm, CategoryForm,UserAddressForm, OrderForm
from .models import UserDetail,ProductVariant
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm, CategoryForm,ProductVariantForm
from .models import UserDetail,CartItem,Product
import random
import requests
from django.core.paginator import Paginator
from decimal import Decimal,InvalidOperation
from django.db.models import Q, F
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views import View
#33333333333333333333333333333333333333333333333333333333333333333333


from django.shortcuts import render, redirect

from .models import UserDetail, Product, Category, Cart, CartItem, Address, Order, Wishlist
from django.contrib.auth.models import User
import requests, random
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.db.models.functions import ExtractMonth, ExtractDay
from django.db.models import Count
import calendar
import io
import razorpay
from datetime import datetime, time, timedelta
from django.http import FileResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template.loader import render_to_string

import os 
import datetime

import requests
from django.template.loader import get_template

from datetime import datetime
from django.db import models
from django.db.models import Sum
from io import BytesIO


# Your code here



# def test(request):
#     return render(request,'user_otp.html')
def cart_item_count(request):
    if 'username' in request.session:
        cart_item_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_item_count = 0
    return {'cart_item_count': cart_item_count}

@never_cache
def base_file(request): 
    obj = Banner.objects.all()
    products=Product.objects.all()[::12]
    
    return render(request, 'index.html',{'obj':obj,'products':products})
    
@never_cache
def user_login(request):
    if 'username' in request.session:
        return redirect('base_file')
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = UserDetail.objects.get(uname=username)
        except UserDetail.DoesNotExist:
            messages.info(request, 'Invalid username or password')
            return redirect('user_login')
        
        if not user.uactive:
            messages.info(request, 'Your account has been blocked')
            return redirect('user_login')
        customer = UserDetail.objects.filter(uname=username).first()
        if not customer and password==customer.upassword:
            messages.info(request, 'Invalid username or passwordddddddddddd')
            return redirect('user_login')
        
        request.session['username'] = username
       
        if 'guest_cart_id' in request.session:
            guest_cart_id = request.session['guest_cart_id']
            guest_user = UserDetail.objects.get(uname='guest')
            cart = NewCart.objects.get(cartid=guest_cart_id)

                            # Associate the cart items with the logged-in user
            cart.user = user
            cart.save()

                            # Clear the guest cart ID from the session
            del request.session['guest_cart_id']

            return redirect('checkout')
        
        return redirect('base_file')

    return render(request, 'user_login.html')



@never_cache
def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('otp_login')

#=============================================== Singup ==================================================================


def generate_otp():
    return str(random.randint(1000, 9999))


def send_otp(phone_num, otp):
    url = 'https://www.fast2sms.com/dev/bulkV2'
    payload = f'sender_id=TXTIND&message={otp}&route=v3&language=english&numbers={phone_num}'
    headers = {
        'authorization': "mEgP0Z5wnldKSerOu1GW8qUbVctH3jkYaM7QCI4Jzp69XNT2ALFmiofRb467D0rSOWVB3qp8J5HYeIvt",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def otp_login(request):
    
    if request.method == 'POST':
        phonenum = request.POST.get('phone')
        user_phonenum_list = UserDetail.objects.values_list('phone', flat=True)
        
        if phonenum not in user_phonenum_list:
            messages.error(request, 'Phone number not found. Please try again.')
            return render(request, 'mobile_otp.html')
        user = UserDetail.objects.get(phone=phonenum)
        if not user.uactive:
            messages.info(request, 'Your account has been blocked')
            return redirect('user_login')
        phonenum = request.POST.get('phone')
        otp = generate_otp()
        
        request.session['U_otp'] = otp
        request.session['U_phone'] = phonenum
        
        send_otp(phonenum, otp)
        
        return redirect('otp_verify')
    return render(request, 'mobile_otp.html')



def otp_verify(request):
    
    if 'U_otp' in request.session and 'U_phone' in request.session:
        exact_otp = request.session['U_otp']
        phonenum = request.session['U_phone']
        if request.method == 'POST':
           
            user_otp = request.POST.get('otp')
            if exact_otp == user_otp:
                try:
                    
                    user = UserDetail.objects.get(phone=phonenum)
                    
                    if user is not None:

                        request.session['username'] = user.uname 
                        request.session['phone'] = phonenum
                        messages.success(request, "Login completed successfully")
                        if 'guest_cart_id' in request.session:
                            guest_cart_id = request.session['guest_cart_id']
                            guest_user = UserDetail.objects.get(uname='guest')
                            cart = NewCart.objects.get(cartid=guest_cart_id)

                            # Associate the cart items with the logged-in user
                            cart.user = user
                            cart.save()

                            # Clear the guest cart ID from the session
                            del request.session['guest_cart_id']

                            return redirect('checkout')
                        
                        return redirect('shop')
                except UserDetail.DoesNotExist:
                    messages.error(request, "This User doesn't Exist")
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        return render(request, 'user_otp.html', {'phonenum': phonenum})
    else:
        return redirect('otp_login')



@never_cache
def req_singup(request):
    if 'username' in request.session:
        del request.session['username']
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('mobile_number')
            otp = generate_otp()
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            request.session['otp'] = otp
            request.session['phone'] = phone
            if not username or username.isspace():
                messages.info(request, 'Username cannot be blank or just spaces.')
            elif len(username) < 4:
                messages.info(request, 'Username must contain at least 4 letters.')
            elif any(char.isdigit() for char in username):
                messages.error(request, 'Username cannot contain numbers.')
            elif UserDetail.objects.filter(uname=username).exists():
                messages.error(request, 'This username is already taken.')
            elif not email or email.isspace():
                messages.info(request, 'Email cannot be blank or just spaces.')
            elif UserDetail.objects.filter(uemail=email).exists():
                messages.error(request, 'This email is already taken.')
            elif not phone or phone.isspace():
                messages.info(request, 'Phone number cannot be blank or just spaces.')
            elif not phone.isdigit() or len(phone) != 10:
                messages.error(request, 'Invalid phone number.')
            elif UserDetail.objects.filter(phone=phone).exists():
                messages.error(request, 'This phone number is already taken.')
            elif password1 != password2:
                messages.error(request, 'Passwords must match.')

            else:
                user_detail = UserDetail(uname=username, uemail=email, upassword=password1, phone=phone)
                user_detail.save()
                form.save()
                user = UserDetail.objects.get(uname=username)
       
        
        
                created = Wallet.objects.get_or_create(user=user, defaults={'balance': 0})
                
                return redirect('otp_login')
    context = {'form': form}
    return render(request, 'singup.html', context)



#========================================Add================================================

def add_variant_prod(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        variant_name = request.POST['variant_name']
        variant_price = request.POST['variant_price']
        variant_stock = request.POST['variant_stock']
        ProductVariant.objects.create(product=product, variant=variant_name, price=variant_price, stock=variant_stock)
        return redirect('admin_page')
    return render(request, 'add_variant.html', {'product': product})

def edit_variants(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    variants = ProductVariant.objects.filter(product=product)
    if request.method == 'POST':
        for variant in variants:
            variant_name = request.POST[f'{variant.id}_name']
            variant_price = request.POST[f'{variant.id}_price']
            variant_stock = request.POST[f'{variant.id}_stock']
            variant.variant = variant_name
            variant.price = variant_price
            variant.stock = variant_stock
            variant.save()
        return redirect('admin_page')
    return render(request, 'edit_variants.html', {'product': product, 'variants': variants})
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

def list_unlist_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        try:
            product = Product.objects.get(id=product_id)
            if action == 'list':
                product.listed = True
            elif action == 'unlist':
                product.listed = False
            product.save()
            # Redirect or show success message

        except Product.DoesNotExist:
            pass
            # Handle product not found error

        # Handle GET request or other cases
    return HttpResponseRedirect(reverse('admin_page'))

def ADD(request):
    if request.method == "POST":
        name = request.POST.get('name').strip()
        description = request.POST.get('description').strip()
        category_id = request.POST.get('category')
        images = request.FILES.getlist('images')

        # Validation
        if not name or name.isspace():
            messages.error(request, 'Name should not be empty or contain only spaces.')
            return redirect('add')
        
        if not description or description.isspace() or len(description) < 10:
            messages.error(request, 'Description should be at least 10 characters long and should not be empty or contain only spaces.')
            return redirect('add')
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category selected.')
            return redirect('add')

        orgi = Product(name=name, category=category, description=description)
        orgi.save()
        for image in images:
            img = Image(image=image, product=orgi)
            img.save()

        messages.success(request, 'Product added successfully.')
        return redirect('admin_page')

    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'add_product.html', context)


#==========================================Edit==============================================
@never_cache
def Edit(request):
    orgi = get_object_or_404(Product, id=id)
    context = {
        'orgi':orgi
    }
    return redirect(request,'edit_product.html',context)

@never_cache
def Update(request, id):
    orgi = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    existing_images = orgi.images.all()

    if request.method == "POST":
        name = request.POST.get("name")
        images = request.FILES.getlist('images') 
        description = request.POST.get("description")
        remove_images = request.POST.getlist('remove_images')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)

        # Validation
        if not name.strip():
            messages.error(request, "Name cannot be empty or contain only spaces.")
        if not description.strip() or len(description.strip()) < 10:
            messages.error(request, "Description should be at least 10 characters long and cannot be empty or contain only spaces.")
        if not category_id:
            messages.error(request, "Category must be selected.")

        if not messages.get_messages(request):
            orgi.name = name
            orgi.description = description
            orgi.category = category
            orgi.save()

            for image in images:
                img = Image(image=image)
                img.save()
                orgi.images.add(img)

            for img_id in remove_images:
                img = Image.objects.get(id=img_id)
                orgi.images.remove(img)

            messages.success(request, "Product updated successfully.")
            return redirect('admin_page')

    context = {
        'orgi': orgi,
        'existing_images': existing_images,
        'categories': categories,
    }
    return render(request, 'edit_product.html', context)

#========================================== Delete=====================================================
@never_cache
def Delete(request,id):
    orgi = Product.objects.filter(id = id)
    orgi.delete()
    
    context ={
        'orgi':orgi,
    }
    return redirect('admin_page')
#==============================user search=====================================
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Product

def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data = [{'name': p.name, 'price': p.normalprice, 'stock': p.stock, 'image': p.image.url, 'category': p.category.name, 'description': p.description} for p in products]
    else:
        data = []
    return JsonResponse({'data': data})

#==============================admin_search==============================
@never_cache
def admin_search(request):
    query = request.GET.get('q').strip()
    context = {}
    if query:
        orgi = Product.objects.filter(name__icontains=query)
    else:
        messages.info(request,'no blank searches allowed')
        return redirect('admin_page')
    context = {
        'orgi': orgi,
        'query': query
    }

    return render(request, 'admin_search.html', context)
#============================================> Admin Login <=============================================


def admin_dash(request):
    if 'adusername' in request.session:
        order=Order.objects.all()
        products=Product.objects.all()
        context={
            'products':products,
            'order':order
        }
        return render(request,'admin_index.html',context)
    else:
        return redirect('admin_login')

@never_cache
def admin_page(request): 
    if 'adusername' in request.session:
        orgi = Product.objects.all()
        categories = Category.objects.all()
       
        context = {
            'orgi': orgi,
             
        'categories': categories}
        
        return render(request,'admin.html',context)
    else:
        return redirect('admin_login')
    
def user_detail(request):

    users = UserDetail.objects.all()
    context = {'users': users}
    return render(request, 'admin_user.html', context)

@never_cache
def admin_login(request):

    if 'adusername' in request.session:
        return redirect('admin_dash')
    if request.method =='POST':
        adusername=request.POST['adusername']
        adpassword=request.POST['adpassword']
        user = MyAdmin.objects.filter(username=adusername, password=adpassword).first()
        if user is not None:
            request.session['adusername']=adusername
            return redirect('admin_dash')
        else:
            messages.info(request,'Enter Valid User Name or Password')

    return render(request,'admin_login.html')

@never_cache
def admin_logout(request):
    if 'adusername' in request.session:
        del request.session['adusername']
    return redirect('admin_login')


#================================================================


def userblock(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        try:
            user = UserDetail.objects.get(id=uid)
        except UserDetail.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('user_detail')
        
        if user.uactive:
            user.uactive = False
            messages.warning(request, f'{user.uname} is blocked')
        else:
            user.uactive = True
            messages.success(request, f'{user.uname} is unblocked')
        user.save()
        # if request.session['user.username'] == user.uname:
        #     del request.session['user.username']
        return redirect('user_detail')
    else:
        return redirect('adminlogin')

#====================================================================================
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_details(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('shop')
    return render(request, 'product_detail.html', {'product': product})


from django.db.models import Prefetch

def category_list(request, category_id=None):
    if category_id is not None:
        categories = Category.objects.prefetch_related(Prefetch('product_set', queryset=Product.objects.all().order_by('-id')))
    else:
        categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category.html', context)

def give_offer_view(request, category_id):
    if request.method == 'POST':
        category = Category.objects.get(pk=category_id)
        offer_percentage = int(request.POST.get('offer_percentage'))
        
        if offer_percentage == 0:
            category.remove_offer()
        else:
            category.give_offer(offer_percentage)
        
        return redirect('category_list',category_id=category_id)  # Redirect to the category list view

def remove_offer_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.remove_offer()
    return redirect('category_list')

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    context = {'form': form}
    return redirect('category_list')

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    context = {'category': category}
    return redirect('category_list')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Category.objects.filter(name=name).exists():
                messages.error(request, 'Category with this name already exists.')
            else:
                Category.objects.create(name=name)
                messages.success(request, 'Category added successfully.')
                return redirect('category_list')
        else:
            messages.error(request, 'Name Already Taken.')
    else:
        form = CategoryForm()
    context = {'form': form}
    return redirect('category_list')
    


#======================================== CART =======================================================================


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cart, CartItem, Product, UserDetail

def shop(request):

        products=Product.objects.all()
        cat=Category.objects.all()
        cat_id = request.GET.get('cat_id')
        prod = request.GET.get('prod_id')
        if cat_id is not None and prod is None:
            details3=Product.objects.filter(category__id=cat_id, listed=True)
        elif prod is not None and cat_id is None:
            details3=Product.objects.filter(name__icontains=prod, listed=True)      
        elif prod is not None and cat_id is not None:
            details3=Product.objects.filter(name__icontains=prod,category__id=cat_id, listed=True)
        else:
            details3=Product.objects.filter(listed=True)

        paginator = Paginator(details3, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index_user.html', {'page_obj': page_obj,'cat':cat,'products':products})


from django.shortcuts import get_object_or_404, redirect
from .models import NewCart, NewCartItem, Product, ProductVariant

def add_to_cart(request):
    if 'username' in request.session:
        username = request.session['username']
        user = UserDetail.objects.get(uname=username)

        if not user.uactive:
            messages.info(request, 'Your account has been blocked')
            return redirect('shop')

        if request.method == 'POST':
            variant_id = request.POST.get('variant_id')

            variant = get_object_or_404(ProductVariant, id=variant_id)

            if variant.stock < 1:
                messages.warning(request, 'Out of stock')
                return redirect('shop')

            cart, _ = NewCart.objects.get_or_create(user=user)

            # Check if the cart already has the same product variant
            cart_item = NewCartItem.objects.filter(cart=cart, variant=variant).first()

            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
            else:
                # If the product variant is not in the cart, create a new cart item
                cart_item = NewCartItem.objects.create(cart=cart, user=user, product=variant.product, variant=variant)

            variant.stock -= 1
            variant.save()

            return redirect('cart')
    else:
        # User is not logged in
        if request.method == 'POST':
            variant_id = request.POST.get('variant_id')
            variant = get_object_or_404(ProductVariant, id=variant_id)

            if variant.stock < 1:
                messages.warning(request, 'Out of stock')
                return redirect('shop')

            # Create a guest user or retrieve an existing one
            guest_user, _ = UserDetail.objects.get_or_create(uname='guest')
            cart, _ = NewCart.objects.get_or_create(user=guest_user)

            # Check if the cart already has the same product variant
            cart_item = NewCartItem.objects.filter(cart=cart, variant=variant).first()

            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
            else:
                # If the product variant is not in the cart, create a new cart item
                cart_item = NewCartItem.objects.create(cart=cart, user=guest_user, product=variant.product, variant=variant)

            variant.stock -= 1
            variant.save()

            # Save the cart ID in the session
            request.session['guest_cart_id'] = cart.cartid

            return redirect('cart')
        
    return redirect('user_login')
    

from .models import NewCart, NewCartItem, Variant


#--------------------------------------------------------------------------------------
def remove_variant_from_cart(request, variant_id):
    if 'username' in request.session:
        username = request.session['username']
        user = UserDetail.objects.get(uname=username)

        if not user.uactive:
            messages.info(request, 'Your account has been blocked')
            return redirect('shop')

        cart = NewCart.objects.filter(user=user).first()
        variant = ProductVariant.objects.get(id=variant_id)  # Assuming you have a Variant model

        if cart:
            cart_item = NewCartItem.objects.filter(cart=cart, variant=variant).first()
            if cart_item:
                cart_item.delete()
                messages.success(request, 'Variant removed from cart successfully.')
            else:
                messages.error(request, 'Variant does not exist in cart.')
        else:
            messages.error(request, 'Cart does not exist.')
            return render(request, 'empty.html')

    return redirect('cart')

def itemcalculate(name):
    total=0
    quantity=0
    set1=UserDetail.objects.filter(uname=name).first()
    set2=set1.id
    data=NewCartItem.objects.filter(cart__user__id=set2)
    for d in data:
        x=int(d.variant.price)
        y=int(d.quantity)
        total += (x*y)
        quantity += d.quantity
    datap={
        "total":total,
        "quantity":quantity
    }
    return({'data':data, 'datap':datap})

from django.http import JsonResponse

def increment_quantity(request, variant_id):
    cart_item = get_object_or_404(NewCartItem, variant_id=variant_id)
    cart_item.quantity += 1
    cart_item.save()

    # Calculate new subtotal
    subtotal = cart_item.quantity * cart_item.variant.price

    return JsonResponse({'subtotal': subtotal})

def decrement_quantity(request, variant_id):
    cart_item = get_object_or_404(NewCartItem, variant_id=variant_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        return JsonResponse({'status': 'deleted'})

    # Calculate new subtotal
    subtotal = cart_item.quantity * cart_item.variant.price

    return JsonResponse({'subtotal': subtotal})
def cart(request):
    if 'username' in request.session:
        username = request.session['username']
        user = UserDetail.objects.get(uname=username)

        if not user.uactive:
            messages.info(request, 'Your account has been blocked')
            return redirect('shop')

        cart = NewCart.objects.filter(user=user).first()
        
       

        if cart:
            cart_items = cart.items.all()
            subtotal_list = []
            total_price = 0
            total_quantity = 0
            for item in cart_items:
                subtotal = item.quantity * item.variant.price  # Assuming the product price is stored in the 'price' field
                subtotal_list.append(subtotal)
                item.subtotal = subtotal
                total_price =total_price+ subtotal
                total_quantity =total_quantity+ item.quantity
        else:
            cart_items = []
            subtotal_list = []
            total_price = 0
            total_quantity = 0
            return render(request,'empty.html')

        context = {
            'cart_items': cart_items,
            'subtotal_list': subtotal_list,
            'total_price': total_price,
            'total_quantity': total_quantity,

        }
        return render(request, 'cart.html', context)
    else:
        # User is not logged in
        guest_cart_id = request.session.get('guest_cart_id')
        if guest_cart_id:
            guest_user = UserDetail.objects.get(uname='guest')
            cart = NewCart.objects.get(cartid=guest_cart_id)
            cart_items = cart.items.all()

            subtotal_list = []
            total_price = 0
            total_quantity = 0

            for item in cart_items:
                subtotal = item.quantity * item.variant.price  # Assuming the product price is stored in the 'price' field
                subtotal_list.append(subtotal)
                item.subtotal = subtotal
                total_price += subtotal
                total_quantity += item.quantity

            context = {
                'cart_items': cart_items,
                'subtotal_list': subtotal_list,
                'total_price': total_price,
                'total_quantity': total_quantity,
            }

            return render(request, 'cart.html', context)

        else:
            # Guest user has no items in the cart
            return render(request, 'empty.html')
        
    
def update_subtotal_and_totals(request, variant_id):
    # Retrieve the necessary data
    cart_item = get_object_or_404(NewCartItem, variant_id=variant_id)

    # Perform calculations
    subtotal = cart_item.quantity * cart_item.variant.price

    # Update the cart item's subtotal
    cart_item.subtotal = subtotal
    cart_item.save()

    # Calculate total quantity and total price for the cart
    cart = cart_item.cart
    cart_items = cart.items.all()
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.subtotal for item in cart_items)

    # Return the updated subtotal, total quantity, and total price as a JSON response
    return JsonResponse({
        'subtotal': subtotal,
        'total_quantity': total_quantity,
        'total_price': total_price,
    })
def update_cart(request):
    if request.method == 'GET':
        user = request.user
        cart_item_id = request.GET.get('cart_item_id')
        quantity = request.GET.get('quantity')
        
        cart_item = NewCartItem.objects.get(Q(id=cart_item_id) & Q(cart__user=user))
        cart_item.quantity = int(quantity)
        cart_item.save()
        
        data = {
            'success': True,
            'subtotal': cart_item.get_total_price,
        }
        
        return JsonResponse(data)



def delcartitems(request):
    if 'username' in request.session:
        id=request.GET['id']
        it=CartItem.objects.get(cartitemid=id)
        if it.quantity<=0:
            return render (request,'empty.html')
        cart_quantity = it.quantity
        cart_product = it.product.name
        Product.objects.filter(name=cart_product).update(stock=F('stock')+cart_quantity)
        CartItem.objects.filter(cartitemid=id).delete()
        return redirect('cart')
    else:
        return redirect('userlogin')
def empty(request):
    return render(request, 'empty.html')



def plus_cart(request):
    if request.method == 'GET':
        use = request.session['username']
        user = UserDetail.objects.get(uname = use)
        prod_id=request.GET['prod_id']
        c = NewCartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        c.quantity+=1
        c.save()
        ProductVariant.objects.filter(id=prod_id).update(stock=F('stock') - 1)
        d = NewCartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        sub = d.get_total_price
        ret = itemcalculate(use)
        datap = {
            'total': ret['datap']['total'],
            'quantity': ret['datap']['quantity'],
            'ind_subtotal': sub,
        }
        return JsonResponse(datap)
    
def minus_cart(request):
    if request.method == 'GET':
        use = request.session['username']
        user = UserDetail.objects.get(uname = use)
        prod_id=request.GET['prod_id']
        c = NewCartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        c.quantity-=1
        c.save()
        Product.objects.filter(id=prod_id).update(stock=F('stock') + 1)
        d = NewCartItem.objects.get(Q(product=prod_id) & Q(cart__user=user))
        sub = d.subtotal
        ret = itemcalculate(use)
        datap = {
            'total': ret['datap']['total'],
            'quantity': ret['datap']['quantity'],
            'ind_subtotal': sub,
        }
        return JsonResponse(datap)
    



#######################################################################################################
# def checkout(request):
#     if 'username' in request.session:
#         if request.method=='POST':
#             if 'addressform' in request.POST:
#                 fm = UserAddressForm(request.POST) 
#                 if fm.is_valid():
#                     use = request.session['username']
#                     user = UserDetail.objects.get(uname = use)
#                     reg = fm.save(commit=False)
#                     reg.user = user
#                     reg.save()
#                     messages.success(request, 'new address added successfully')
#                     return redirect('checkout') 
#                 else:
#                     messages.warning(request,'Enter correct address') 
#                     return render(request, 'checkout.html', {'fm': fm})
#             elif 'couponform' in request.POST:
#                 check = request.POST.get('c_code')
#                 uname=request.session['username']
#                 try:
#                     obj = Coupon.objects.get(is_active=True,coupon_code=check)
#                 except:
#                     messages.warning(request,'No coupon')
#                     return redirect('checkout')
#                 # if check==obj.coupon_code and obj.is_active:
#                 #     Coupon.objects.filter(user__uname=uname).update(applied=False)
#                 #     Coupon.objects.filter(user__uname=uname,is_active=True,coupon_code=check).update(applied=True)
#                 if check==obj.coupon_code and obj.is_active:
#                     pass
#                 else:
#                     messages.warning(request,'Coupon is not valid')
#                 return redirect('checkout')            
#         else:
#             fm = UserAddressForm()
#             use = request.session['username']

#             context=Address.objects.filter(user__uname = use).order_by('-id')

#             try:
#                 coup = Coupon.objects.get(is_active=True,applied=True)
#                 ret = itemcalculate(use)
#                 disc = ret['datap']['total']
#                 applied_discount = disc - coup.discount_price
#             except Coupon.DoesNotExist:
#                 coup = None
#                 ret = itemcalculate(use)
#                 disc = ret['datap']['total']
#                 applied_discount = disc - 0
#             except:
#                 coup = Coupon.objects.get(is_active=True)
#                 ret = itemcalculate(use)
#                 disc = ret['datap']['total']
#                 applied_discount = disc - 0
#             if disc<=0:
#                 messages.warning(request,'Order total is less than or equal to zero')
#                 return redirect('cart')
#             coupon = Coupon.objects.filter(is_active=True)
#             return render(request, 'checkout.html', {'fm': fm, 'context': context, 'data':ret['data'], 'datap':ret['datap'],'coup':coup,'disc':applied_discount,'coupon':coupon})
#     else:
#         return redirect('user_login')
def checkout(request):
    if 'username' in request.session:
        if request.method=='POST':
            if 'addressform' in request.POST:
                fm = UserAddressForm(request.POST) 
                if fm.is_valid():
                    use = request.session['username']
                    user = UserDetail.objects.get(uname = use)
                    reg = fm.save(commit=False)
                    reg.user = user
                    reg.save()
                    messages.success(request, 'new address added successfully')
                    return redirect('checkout') 
                else:
                    messages.warning(request,'Enter correct address') 
                    return render(request, 'checkout.html', {'fm': fm})
            elif 'couponform' in request.POST:
                check = request.POST.get('c_code')
                minimum_amount = Coupon.objects.get(is_active=True).minimum_amount
                
                if not check:
                    messages.warning(request, 'Please enter a coupon code')
                    return redirect('checkout')

                if minimum_amount > 0:
                    # Check if the order total is less than the minimum amount
                    ret = itemcalculate(request.session['username'])
                    total = ret['datap']['total']
                    if total < minimum_amount:
                        messages.warning(request, f'Total amount must be greater than or equal to {minimum_amount}')
                        return redirect('checkout')

                try:
                    obj = Coupon.objects.get(coupon_code=check, is_active=True)
                except Coupon.DoesNotExist:
                    messages.warning(request, 'Invalid coupon')
                    return redirect('checkout')

                if obj.applied:
                    messages.warning(request, 'Coupon already applied')
                    
                    return redirect('checkout')
                else:
                    Coupon.objects.filter(is_active=True).update(applied=False)
                    obj.applied = True
                    obj.is_active=False
                    obj.save()
                    messages.success(request, 'Coupon applied successfully')

                return redirect('checkout')            
        else:
            fm = UserAddressForm()
            use = request.session['username']

            context=Address.objects.filter(user__uname = use).order_by('-id')

            try:
                coup = Coupon.objects.get(is_active=True, applied=True)
                ret = itemcalculate(use)
                disc = ret['datap']['total']
                applied_discount = disc - coup.discount_price
            except Coupon.DoesNotExist:
                coup = None
                ret = itemcalculate(use)
                disc = ret['datap']['total']
                applied_discount = disc - 0
            except:
                coup = Coupon.objects.get(is_active=True)
                ret = itemcalculate(use)
                disc = ret['datap']['total']
                applied_discount = disc - 0

            if disc <= 0:
                messages.warning(request, 'Order total is less than or equal to zero')
                return redirect('cart')

            coupon = Coupon.objects.filter(is_active=True)
            return render(request, 'checkout.html', {'fm': fm, 'context': context, 'data': ret['data'], 'datap': ret['datap'], 'coup': coup, 'disc': applied_discount, 'coupon': coupon})
    else:
        return redirect('user_login')
    
def updateaddress(request,id):
    if 'username' in request.session:
        add = Address.objects.get(id=id)
        if request.method == 'POST':
            fm = UserAddressForm(request.POST, instance=add)
            if fm.is_valid():
                fm.save()
                messages.success(request,"Address updated successfully")
                return redirect('checkout')
            else:
                return render(request, 'updateaddress.html', {'fm': fm})
        else:
            fm = UserAddressForm(instance=add)
            use = request.session['username']
            context=Address.objects.filter(user__uname = use)
            ret = itemcalculate(use)
            return render(request, 'updateaddress.html', {'fm': fm, 'context': context, 'data':ret['data'], 'datap':ret['datap']})
    else:
        return redirect(request,'user_login')

def deleteaddress(request):
    if 'username' in request.session:
        uid=request.GET['uid']
        Address.objects.filter(id=uid).delete()
        return redirect('checkout')
    else:
        return redirect('user_login')

def address_select(request):
    if 'username' in request.session:
        uid=request.GET['uid']
        select_check=Address.objects.filter(id=uid)
        for x in select_check:
            if x.selected:
                Address.objects.filter(id=uid).update(selected=False)
                messages.warning(request, f'{x.name} is Unselected')
            else:
                Address.objects.all().update(selected=False)
                Address.objects.filter(id=uid).update(selected=True)
                messages.success(request, f'{x.name} is Selected')
        return redirect('checkout')
    else:
        return redirect('otp_login')
    
    
from django.db.models import F

def order(request):
    if 'username' in request.session:
        user = request.session['username']
        user = UserDetail.objects.get(uname = user)
        ord = Order.objects.filter(user=user).order_by('-id')
        paginator = Paginator(ord, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        if ord.exists():
            return render(request,'order.html',{'page_obj':page_obj})
        else:
            messages.warning(request,'No orders found')
            return redirect('empty')
    else:
        return redirect('user_login')
    
def orderconfirm(request):
    if 'username' in request.session:    
        user = request.session['username']
        use1 = UserDetail.objects.get(uname = user)
        try:
            use2 = Address.objects.get(user=use1,selected=True)
        except:
            messages.warning(request,'No address specified')
            return redirect('checkout')
        cart = NewCartItem.objects.filter(cart__user__uname=use1)
        try:
            coupon = Coupon.objects.get(user=use1,is_active=True,applied=True)
            discount = coupon.discount_price
        except:
            discount = 0
        cartcount = cart.count()
        for c in cart:
            Order(user=use1, address=use2,variant=c.variant, product=c.product, amount=c.get_total_price-(discount)/cartcount).save()
            c.delete() 
        return render(request,'orderconfirm.html')
    else:
        return redirect('otp_login')
    
def cancelorder(request,id):
    if 'username' in request.session:  
        Order.objects.filter(id=id).update(status='Cancel Requested')
        return redirect('order')
    else:
        return redirect('user_login')

def returnorder(request,id):
    if 'username' in request.session: 
        Order.objects.filter(id=id).update(status='Return Requested')
        return redirect('order')
    else:
        return redirect('otp_login')


def adminorderlist(request):
    if 'adusername' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            member=Order.objects.filter(Q(user__uname__icontains=search)|Q(id__icontains=search)).order_by('-id')
        else:
            member = Order.objects.all().order_by('-id')
        paginator = Paginator(member, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'adminorderlist.html', {'page_obj': page_obj})
    else:
        return redirect('admin_login')
    
class OrderUpdateView(View):
    def get(self, request, id):
        if 'adusername' in request.session:
            ord = Order.objects.get(id=id)
            fm = OrderForm(instance=ord)
            return render(request, 'adminupdateorder.html', {'fm': fm})
        else:
            return redirect('admin_login')

    def post(self, request, id):
        if 'adusername' in request.session:
            ord = Order.objects.get(id=id)
            fm = OrderForm(request.POST, request.FILES, instance=ord)
            if fm.is_valid():
                fm.save()
                return redirect('adminorderlist')
            else:
                return render(request, 'adminupdateorder.html', {'fm': fm})
        else:
            return redirect('admin_login')


def shopsingle(request):
    uid = request.GET.get('uid')
    product = Product.objects.prefetch_related('images').filter(id=uid).first()
    images = product.images.all() if product else []
    variants = ProductVariant.objects.filter(product=product).order_by('price')
    products_in_same_category = Product.objects.filter(category=product.category)
    category_offer_percentage = None
    if product.category:
        category_offer_percentage = product.category.offer_percentage
    return render(request, 'product_detail.html', {'product': product, 'images': images,'variants': variants, 'products_in_same_category':products_in_same_category,'category_offer_percentage':category_offer_percentage})



from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Variant
from .forms import VariantForm

class VariantView(TemplateView):
    template_name = 'variant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.all()
        context['form'] = VariantForm()
        return context

class AddVariantView(CreateView):
    model = Variant
    form_class = VariantForm
    template_name = 'variant.html'
    success_url = reverse_lazy('variant')

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class EditVariantView(UpdateView):
    model = Variant
    form_class = VariantForm
    template_name = 'variant.html'
    success_url = reverse_lazy('variant')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variant_id_being_edited'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Variant updated successfully')
        return response

class DeleteVariantView(DeleteView):
    model = Variant
    template_name = 'variant.html'
    success_url = reverse_lazy('variant')
        
# def list_product(request,id):
#     product = get_object_or_404(Product, id=id)
#     product.listed = True
#     product.save()
#     return redirect('product_detail', id=id)

# # view function to unlist a product
# def unlist_product(request,id):
#     product = get_object_or_404(Product, id=id)
#     product.listed = False
#     product.save()
#     return redirect('product_detail', id=id)



def userprofile(request):
    if 'username' in request.session:       
        user=request.session['username']
        profile=UserDetail.objects.get(uname=user)
        address=Address.objects.filter(user__uname=user).order_by('id')
        return render(request, 'userprofile.html',{'profile':profile,'address':address})
    else:
        return redirect('user_login')
    
class EditUserProfileView(View):
    def get(self, request):
        if 'username' in request.session:
            user = request.session['username']
            user = UserDetail.objects.get(uname=user)
            return render(request, 'edituserprofile.html', {'user': user})
        else:
            return redirect('user_login')

    def post(self, request):
        if 'username' in request.session:   
            user = request.session['username']
            user = UserDetail.objects.get(uname=user)
            uemail = request.POST.get('uemail')
            uphone = request.POST.get('uphone')
            UserDetail.objects.filter(uname=user.uname).update(uemail=uemail, phone=uphone)
            messages.success(request, 'User details updated successfully')
            return redirect('userprofile')
        else:
            return redirect('user_login')
        
class ChangePasswordView(View):
    def get(self, request):
        if 'username' in request.session:   
            return render(request,'changepassword.html')
        else:
            return redirect('user_login')   
    def post(self, request):
        if 'username' in request.session:
            user = request.session['username']
            user = UserDetail.objects.get(uname=user) 
            password = request.POST.get('upassword')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            if user.upassword == password:
                if pass1 == pass2:
                    if ' ' not in pass1:  # Check for spaces in the new password
                        user.upassword = pass1
                        user.save()
                        messages.success(request, "Passwords changed successfully")
                        return redirect('userprofile')
                    else:
                        messages.warning(request, "Passwords should not contain spaces")
                else:
                    messages.warning(request, "Passwords not matching")
            else:
                messages.warning(request, "Incorrect password")
            return redirect('changepassword')
        else:
            return redirect('user_login')

def updateprofileaddress(request,id):
    if 'username' in request.session:
        add = Address.objects.get(id=id)
        if request.method == 'POST':
            fm = UserAddressForm(request.POST, instance=add)
            if fm.is_valid():
                fm.save()
                messages.success(request,"Address updated successfully")
                return redirect('userprofile')
            else:
                return render(request, 'updateprofileaddress.html', {'fm': fm})
        else:
            fm = UserAddressForm(instance=add)
            return render(request, 'updateprofileaddress.html', {'fm': fm})
    else:
        return redirect('user_login')
    
def addprofileaddress(request):
    if 'username' in request.session:
        if request.method=='POST':
            fm = UserAddressForm(request.POST) 
            if fm.is_valid():
                use = request.session['uname']
                user = UserDetail.objects.get(uname = use)
                reg = fm.save(commit=False)
                reg.user = user
                reg.save()
                messages.success(request, 'new address added successfully')
                return redirect('userprofile') 
            else:
                return render(request, 'addprofileaddress.html', {'fm': fm})
        else:
            fm = UserAddressForm()
            return render(request, 'addprofileaddress.html', {'fm': fm})
    else:
        return redirect('user_login')
    


def wishlist(request):
    if 'username' in request.session:
        wish_id = request.GET.get('wish_id')
        if wish_id is not None:
            wish_product = Product.objects.get(id=wish_id)
            dup = Wishlist.objects.filter(product__name=wish_product.name).first()
            if dup is None:
                product = Product.objects.get(id=wish_id)
                use1 = request.session['username']
                use2 = UserDetail.objects.get(uname=use1)
                wish = Wishlist(user=use2,product=product)
                wish.save()
                wish_items = Wishlist.objects.all().order_by('-id')
            else:
                messages.warning(request,'Item is already in the wishlist')
                wish_items = Wishlist.objects.all().order_by('-id')
        else:
            wish_items = Wishlist.objects.all().order_by('-id')
        if wish_items.exists():
            return render(request,'wishlist.html',{'wish_items':wish_items})
        else:
            messages.warning(request,'No items in wishlist')
            return render (request,'empty.html')
    else:
        return redirect('user_login')



def wishlistdelete(request,id):
    if 'username' in request.session:
        Wishlist.objects.filter(id=id).delete()
        return redirect('wishlist')
    else:
        return redirect('user_login')

def paypal(request):
    
    if 'username' in request.session:
        user = request.session['username']
        use1 = UserDetail.objects.get(uname = user)
        try:
            use2 = Address.objects.get(user=use1,selected=True)
        except:
            messages.warning(request,'No address specified')
            return redirect('checkout')
        cart = NewCartItem.objects.filter(cart__user__uname=use1)
        for c in cart:
            Order(user=use1, address=use2, product=c.product, amount=c.get_total_price, ordertype= 'Paypal').save()
            c.delete()
        return render(request,'orderconfirm.html')
    else:
        return redirect('user_login')


def razorpay(request):
    client = razorpay.Client(auth=("rzp_test_fe92PDGUR6EoGd", "FDZuKaPhHQvQnBT4u8rJ9M2e"))
    DATA = {
        "amount": 100 ,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }

    razorpay_response=client.order.create(data=DATA)

    reazorpay_status=razorpay_response['status']
    if reazorpay_status == 'created':
        if 'username' in request.session:
            user = request.session['username']
            use1 = UserDetail.objects.get(uname = user)
            try:
                use2 = Address.objects.get(user=use1,selected=True)
            except:
                messages.warning(request,'No address specified')
                return redirect('checkout')
            cart = NewCartItem.objects.filter(cart__user__uname=use1)
            for c in cart:
                Order(user=use1, address=use2, product=c.product, amount=c.get_total_price, ordertype= 'Paid From Your Wallet').save()
                c.delete()
            return render(request,'orderconfirm.html')
        else:
            return redirect('user_login')
    else:
        messages.warning(request,'Something wrong')
        return redirect('shop')



def cancelcoupon(request):
    Coupon.objects.filter(is_active=True).update(applied=False)
    messages.warning(request, 'Coupon removed')
    return redirect('checkout')


def admincouponlist(request):
    if 'username' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            member=Coupon.objects.filter(coupon_code__icontains=search)
        else:
            member=Coupon.objects.all().order_by('-id')
        return render(request,'admincouponlist.html',{'member': member})
    else:
        return render(request, 'adminlogin.html')
    
def adminaddcoupon(request):
    if 'username' in request.session:       
        if request.method == 'POST':
            fm = CouponForm(request.POST,request.FILES)
            if fm.is_valid():
                coupon_code = fm.cleaned_data['coupon_code']
                dup = Coupon.objects.filter(coupon_code=coupon_code).first()
                if dup:
                    messages.warning(request,'Coupon already exists')
                    return redirect('adminaddcoupon')
                else: 
                    fm.save()
                    return redirect('admincouponlist')       
        else:        
            fm = CouponForm()
            return render(request, 'adminaddcoupon.html',{'fm':fm})
    else:
        return render(request, 'adminlogin.html')

def deletecoupon(request):
    if 'username' in request.session:
        uid=request.GET['uid']
        Coupon.objects.filter(id=uid).delete()
        return redirect('admincouponlist')
    else:
        return redirect('adminlogin')

def updatecoupon(request):
    if 'username' in request.session:
        uid = request.GET['uid']
        cat = Coupon.objects.get(id=uid)
        if request.method == 'POST':
            fm = CouponForm(request.POST, request.FILES, instance=cat)
            if fm.is_valid():
                fm.save()
                return redirect('admincouponlist')
        else:
            fm = CouponForm(instance=cat)
            return render(request, 'adminupdatecoupon.html', {'fm': fm})
    else:
        return redirect('adminlogin')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle,Table
from reportlab.lib import colors
import pandas as pd
import openpyxl
def sales_report(request):
    if request.method == 'POST':    
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        generate = request.POST.get('generate')
        if not start_date or not end_date:
            messages.warning(request, 'Check dates')
            return redirect('sales_report')
        if end_date < start_date:
            messages.warning(request, 'start date is not less than end date')
            return redirect('sales_report')
        elif end_date >= start_date:
            if generate=='PDF':
                buf = io.BytesIO()
                c = canvas.Canvas(buf,pagesize=letter, bottomup=1)
                textob = c.beginText()
                textob.setTextOrigin(inch, inch)
                textob.setFont("Helvetica", 16)
                orders = Order.objects.all()
                if start_date and end_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                    orders = orders.order_by('-ordered_date').filter(ordered_date__range=[start_date, end_date])
                else:
                    orders = Order.objects.all().order_by('-order_date')
                if not orders.exists():
                    messages.warning(request,'No data found')
                    return redirect('sales_report')           
                table_header = ["Customer Name", "Product Title", "Order Date and Time", "Order Status", "Payment Status"]            
                table_data = []
                for ord in orders:
                    row_data = [ord.address.user.uname, ord.product.name, str(ord.ordered_date), str(ord.status), str(ord.ordertype)]
                    table_data += [row_data]
                pdfTable = Table([table_header] +table_data)           
                pdfTableStyle = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightblue)]) 
                pdfTable.setStyle(pdfTableStyle)
                pdfTable.wrapOn(c, 100, 100)
                pdfTable.drawOn(c, 10, 10 + 5)
                c.drawText(textob)
                c.showPage()
                c.save()
                buf.seek(0)
                return FileResponse(buf, as_attachment=True, filename="Sales report.pdf")

            else:
                orders = Order.objects.filter(ordered_date__range=[start_date, end_date])
                if not orders.exists():
                    messages.warning(request,'No data found')
                    return redirect('sales_report') 
                orders_df = pd.DataFrame(list(orders.values()))
                try:
                    orders_df.drop(['user_id', 'address_id'], axis=1, inplace=True)
                except:
                    messages.warning(request,'Something wrong')
                    return redirect('sales_report')
                orders_df.rename(columns={'product_id': 'product_id', 'amount': 'amount', 'ordered_date': 'ordered_date', 'ordertype': 'order_type', 'status': 'status'}, inplace=True)
                orders_df['ordered_date'] = orders_df['ordered_date'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
                orders_df.to_excel(response, index=False)
                return response   
            
        else:
            print("!!Unidentified")
    else:
        return render(request,'sales_report.html')

def handle_not_found(request,exception):
    return render(request,'not-found.html')

from xhtml2pdf import pisa

def generateinvoice(request):
    user = UserDetail.objects.get(uname = request.session['username'])

    ordered_product = Order.objects.get(Q(id=request.GET.get('ord_id')) & Q(user=user))  
    data = {
        # 'date' : datetime.date.today(),
        'orderid': ordered_product.id,
        'ordered_date': ordered_product.ordered_date,
        'name': ordered_product.address.name,
        'housename': ordered_product.address.housename,
        'locality' : ordered_product.address.locality,
        'city' : ordered_product.address.city, 
        'state' : ordered_product.address.state, 
        'zipcode': ordered_product.address.zipcode,
        'phone' : ordered_product.address.phone,
        'product': ordered_product.product.name,
        'amount' : ordered_product.amount,
        'ordertype': ordered_product.ordertype,
    } 
    template_path = 'invoicepdf.html'
    context = {
        # 'date': data['date'],
        'orderid': data['orderid'],
        'name': data['name'],
    }
    html = render_to_string(template_path, data)
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{data["orderid"]}.pdf"'
  

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def adminbannerlist(request):
    if 'username' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            member=Banner.objects.filter(name__icontains=search)
        else:
            member=Banner.objects.all().order_by('-id')
        return render(request,'adminbannerlist.html',{'member': member})
    else:
        return render(request, 'adminlogin.html')
    
def updatebanner(request):
    if 'username' in request.session:
        uid = request.GET['uid']
        cat = Banner.objects.get(id=uid)
        if request.method == 'POST':
            fm = BannerForm(request.POST, request.FILES, instance=cat)
            if fm.is_valid():
                fm.save()
                return redirect('adminbannerlist')
        else:
            fm = BannerForm(instance=cat)
            return render(request, 'adminupdatebanner.html', {'fm': fm})
    else:
        return redirect('adminlogin')

def adminaddbanner(request): 
    if 'username' in request.session:
        if request.method == 'POST':
            fm = BannerForm(request.POST, request.FILES)
            if fm.is_valid():
                fm.save()
                return redirect('adminbannerlist')
            else:
                return render(request, 'adminaddbanner.html', {'fm': fm})
        else:
            fm = BannerForm()
            return render(request, 'adminaddbanner.html', {'fm': fm})
    else:
        return redirect('adminlogin')
    
def deletebanner(request):
    if 'username' in request.session:
        uid=request.GET['uid']
        Banner.objects.filter(id=uid).delete()
        return redirect('adminbannerlist')
    else:
        return redirect('adminlogin')

def wallet_balance_view(request):
    username = request.session['username']
    wallet = Wallet.objects.get(user__uname=username)
    transactions = wallet.get_transaction_history()
    context = {
        'user': wallet.user.uname,
        'balance': wallet.balance,
        'transactions': transactions
    }
    return render(request, 'wallet_balance.html', context)

def deposit_view(request):
    if request.method == 'POST':
        username = request.session['username']
        user = UserDetail.objects.get(uname=username)
        amount =  Decimal(request.POST.get('amount'))
        
        # Retrieve or create the wallet for the user
        wallet, created = Wallet.objects.get_or_create(user=user, defaults={'balance': 0})
        
        wallet.deposit(amount)
        return redirect('balance')
    return render(request, 'deposit.html')

def withdraw_view(request):
    if request.method == 'POST':
        username = request.session['username']
        user = UserDetail.objects.get(uname=username)
        amount = float(request.POST.get('amount'))
        wallet = Wallet.objects.get(user=user)
        wallet.withdraw(amount)
        return redirect('wallet_balance_view')
    return render(request, 'withdraw.html')

def transfer_view(request):
    if request.method == 'POST':
        username = request.session['username']
        user = UserDetail.objects.get(uname=username)
        amount = float(request.POST.get('amount'))
        recipient= request.POST.get('recipient')
        wallet = Wallet.objects.get(user=user)
        recipient_username=UserDetail.objects.get(uname=recipient)
        recipient_wallet = Wallet.objects.get(user=recipient_username)
        wallet.transfer(amount, recipient_wallet)
        return redirect('wallet_balance_view')
    return render(request, 'transfer.html')

def wallet_payment_view(request):
    if request.method == 'POST':
        username = request.session['username']
        user = UserDetail.objects.get(uname=username)
        amount = request.POST.get('amount')
        amount = float(amount)
        wallet = Wallet.objects.get(user=user)
        if wallet.balance >=  Decimal(str(amount)):
            wallet.withdraw(amount)
            try:
                use2 = Address.objects.get(user=user,selected=True)
            except:
                messages.warning(request,'No address specified')
                return redirect('checkout')
            cart = NewCartItem.objects.filter(cart__user__uname=user)
            for c in cart:
                Order(user=user, address=use2, product=c.product, amount=c.get_total_price, ordertype= 'Paid From Your Wallet').save()
                c.delete()
            
            return redirect('orderconfirm')
        else:
            return render(request, 'insufficient_balance.html')
    return render(request, 'wallet_payment.html')

def product_offer(request, product_id):
    product = Product.objects.get(id=product_id)
    variants = product.productvariant_set.all()

    if request.method == 'POST':
        if 'add_offer' in request.POST:
            offer_percentage = int(request.POST['offer_percentage'])
            product.give_offer(offer_percentage)
            return redirect('product_offer', product_id=product_id)
        elif 'remove_offer' in request.POST:
            product.remove_offer()
            return redirect('product_offer', product_id=product_id)

    context = {
        'product': product,
        'variants': variants,
    }
    return render(request, 'product_offer.html', context)