from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(offer)
admin.site.register(MyAdmin)
admin.site.register(UserDetail)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Variant)
admin.site.register(ProductVariant)
admin.site.register(Wishlist)
admin.site.register(Coupon)
admin.site.register(NewCart)
admin.site.register(NewCartItem)
admin.site.register(NewWishlist)
admin.site.register(Wallet)

