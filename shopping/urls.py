from django.contrib import admin
from django.urls import path
from . import views
from .views import OrderUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import  OrderUpdateView, EditUserProfileView, ChangePasswordView
from .views import VariantView, AddVariantView, EditVariantView, DeleteVariantView
urlpatterns = [
    
    path('user_login',views.user_login,name="user_login"),
    path('',views.base_file,name="base_file"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('search',views.search,name='search'),
    # path('index',views.index,name='index'),
    # path('table',views.table,name='table'),
    # path('contact',views.contact,name='contact'),
    path('req_singup',views.req_singup,name='req_singup'),
    # path('admin_pro',views.admin_pro,name='admin_pro'),
    path('add',views.ADD,name='add'),
    path('edit',views.Edit,name='edit'),
    path('search',views.search,name='search'),
    path('update/<str:id>',views.Update,name='update'),
    
    path('delete/<str:id>',views.Delete,name="delete"),
     path('update_subtotal_and_totals/<int:variant_id>/', views.update_subtotal_and_totals, name='update_subtotal_and_totals'),
    
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_page',views.admin_page,name="admin_page"),
    path('admin_logout',views.admin_logout,name="admin_logout"),

    # path('test',views.test,name="test"),
    path('user_detail',views.user_detail,name="user_detail"),
   
    path('admin_dash',views.admin_dash,name='admin_dash'),

    
    path('category_list/', views.category_list, name='category_list'),
    path('category_list/<int:category_id>/',views.category_list,name='category_list'),
    path('add_category',views.add_category,name='add_category'),
    path('edit_category/<int:category_id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),


    # path('admindashboard/', views.admindashboard, name='admindashboard'),#
    # path('adminuserlist/', views.adminuserlist, name='adminuserlist'),#
    # path('adminproductlist/', views.adminproductlist, name='adminproductlist'),#
    path('userblock/', views.userblock, name='userblock'),
    path('otp_verify', views.otp_verify, name='otp_verify'),
    path('otp_login', views.otp_login, name='otp_login'),

    # path('new_add_to_cart/<int:product_id>/<int:variant_id>/', views.new_add_to_cart, name='new_add_to_cart'),


    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),
    path('empty/', views.empty, name='empty'),
   path('remove_variant_from_cart/<int:variant_id>/', views.remove_variant_from_cart, name='remove_variant_from_cart'),
    path('shop/', views.shop, name='shop'),
    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('updateaddress/<int:id>', views.updateaddress, name='updateaddress'),
    path('deleteaddress/', views.deleteaddress, name='deleteaddress'),
    path('address_select/', views.address_select, name='address_select'),
    path('order/', views.order, name='order'),
    path('orderconfirm/', views.orderconfirm, name='orderconfirm'),
    path('cancelorder/<int:id>', views.cancelorder, name='cancelorder'),
    path('orderconfirm/', views.orderconfirm, name='orderconfirm'),
    path('returnorder/<int:id>', views.returnorder, name='returnorder'),
    path('adminorderlist/', views.adminorderlist, name='adminorderlist'),
    path('updateorder/<int:id>', OrderUpdateView.as_view(), name='updateorder'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    
    path('shopsingle/', views.shopsingle, name='shopsingle'),
    # path('about/', views.about, name='about'),
    # path('product/<int:product_id>/list/', views.list_product, name='list_product'),
    # path('product/<int:product_id>/unlist/', views.unlist_product, name='unlist_product'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('edituserprofile/', EditUserProfileView.as_view(), name='edituserprofile'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
     path('updateprofileaddress/<int:id>', views.updateprofileaddress, name='updateprofileaddress'),
    path('addprofileaddress/', views.addprofileaddress, name='addprofileaddress'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlistdelete/<int:id>', views.wishlistdelete, name='wishlistdelete'),
    # path('sales_report/', views.sales_report, name='sales_report'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('variant/', VariantView.as_view(), name='variant'),
    path('variant/add/', AddVariantView.as_view(), name='variant_add'),
    path('variant/edit/<int:pk>/', views.EditVariantView.as_view(), name='edit_variant'),
    path('variant/delete/<int:pk>/', DeleteVariantView.as_view(), name='delete_variant'),
    path('product/<int:product_id>/add-variants/', views.add_variant_prod, name='add_variants'),
    path('product/<int:product_id>/edit-variants/', views.edit_variants, name='edit_variants'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlistdelete/<int:id>', views.wishlistdelete, name='wishlistdelete'),
    path('cancelcoupon/', views.cancelcoupon, name='cancelcoupon'),
    path('admincouponlist/', views.admincouponlist, name='admincouponlist'),
    path('adminaddcoupon/', views.adminaddcoupon, name='adminaddcoupon'),
    path('deletecoupon/', views.deletecoupon, name='deletecoupon'),
    path('updatecoupon/', views.updatecoupon, name='updatecoupon'),
    path('paypal/', views.paypal, name='paypal'),
    path('razorpay/', views.razorpay, name='razorpay'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('generateinvoice/', views.generateinvoice, name='generateinvoice'),
    path('updatebanner/', views.updatebanner, name='updatebanner'),
    path('adminaddbanner/', views.adminaddbanner, name='adminaddbanner'),
    path('adminbannerlist/', views.adminbannerlist, name='adminbannerlist'),
    path('deletebanner/', views.deletebanner, name='deletebanner'),
    path('increment_quantity/<int:variant_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:variant_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('balance/', views.wallet_balance_view, name='balance'),
    path('wallet_payment/', views.wallet_payment_view, name='wallet_payment'),
    path('give_offer/<int:category_id>/', views.give_offer_view, name='give_offer'),
    path('remove_offer/<int:category_id>/', views.remove_offer_view, name='remove_offer'),
    path('product_offer/<int:product_id>/', views.product_offer, name='product_offer'),
    path('list_unlist_product/', views.list_unlist_product, name='list_unlist_product'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)