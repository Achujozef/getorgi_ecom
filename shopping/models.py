from django.db import models

from decimal import Decimal

# Create your models here.
 
class Category(models.Model):
    name = models.CharField(max_length=50)
    offer_percentage = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.name
    def give_offer(self, offer_percentage):
        self.offer_percentage = offer_percentage
        self.save()
        product_variants = ProductVariant.objects.filter(product__category=self)
        for variant in product_variants:
            variant.update_price_with_offer(offer_percentage)

    def remove_offer(self):
        self.offer_percentage = None
        self.save()
        product_variants = ProductVariant.objects.filter(product__category=self)
        for variant in product_variants:
            variant.restore_original_prices()

class Variant(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, default='')
    stock = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  null=True)
    normalprice = models.IntegerField(default=0)
    listed = models.BooleanField(default=True)
    offer_percentage = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.name
    def give_offer(self, offer_percentage):
        self.offer_percentage = offer_percentage
        self.save()
        product_variants = ProductVariant.objects.filter(product=self)
        for variant in product_variants:
            variant.update_price_with_offer(offer_percentage)
            variant.save()

    def remove_offer(self):
        self.offer_percentage = 0
        self.save()
        product_variants = ProductVariant.objects.filter(product=self)
        for variant in product_variants:
            variant.update_price_with_offer(0)
            variant.save()


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant =models.CharField(max_length=50)
    price = models.IntegerField()
    price_after_offer = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.product.name} - {self.variant} - {self.price}'

    def update_price_with_offer(self, offer_percentage):
        original_price = self.price
        if offer_percentage > 0:
            discounted_price = original_price - (original_price * offer_percentage / 100)
            self.price_after_offer = discounted_price
        else:
            self.price_after_offer = original_price
        self.save()

    def restore_original_prices(self):
        original_price = self.price
        self.price_after_offer = original_price
        self.save()
    def set_price(self, new_price):
        self.price = new_price
        self.update_price_with_offer(self.product.offer_percentage)
        self.save()
        
class Image(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='images', default=None)
    
    
    def __str__(self):
        return self.image.name

class offer(models.Model):
    coupen= models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    discount = models.IntegerField()

    
class MyAdmin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class UserDetail(models.Model):
    uname=models.CharField(unique=True, max_length=50)
    uemail=models.CharField(max_length=50)
    phone=models.CharField(max_length=50, null=True)
    upassword=models.CharField(max_length=50)
    uactive=models.BooleanField(default=True)
    uimage = models.ImageField(upload_to='imagestore/', null=True, blank=True)
    uotp=models.IntegerField(null=True)
    def __str__(self): 
        return self.uname 
    
class Cart(models.Model):
    cartid=models.AutoField(primary_key=True)
    user=models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=False)

class CartItem(models.Model):
    cartitemid=models.AutoField(primary_key=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
    quantity=models.PositiveBigIntegerField()

    @property
    def subtotal(self):
        return int(self.product.price)*int(self.quantity)



class NewCart(models.Model):
    cartid=models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name='carts')

class NewCartItem(models.Model):
    cart = models.ForeignKey(NewCart, on_delete=models.CASCADE, related_name='items')
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    class Meta:
        unique_together = ('cart', 'user', 'variant')

    
    @property
    def get_total_price(self):
        return self.variant.price_after_offer * self.quantity
    




STATE_CHOICES = (
    ('KARNATAKA', 'KARNATAKA'),
    ('KERALA', 'KERALA'),
    ('TAMIL NADU', 'TAMIL NADU'),
    ('GOA', 'GOA'),
    ('GUJARAT', 'GUJARAT')
)
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel Requested', 'Cancel Requested'),
    ('Return Requested', 'Return Requested'),
    ('Cancelled', 'Cancelled'),
    ('Returned', 'Returned'),
)
TYPE_CHOICES = (
    ('Cash on delivery', 'Cash on delivery'),
    ('Online Payment', 'Online Payment'),
    ('Razorpay', 'Razorpay'),
    ('Wallet','Wallet')
)
class Address(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    housename = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50, default='KERALA')
    selected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Order(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordertype = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Cash on delivery')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    variant=models.CharField(max_length=50, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
 
         
class Wishlist(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE,default=None)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE,default=None)
    def __str__(self):
        return (str(self.user.uname) + str(" , ") +str(self.product.name))
    
class NewWishlist(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, default=None)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.user.uname} - {self.variant.product.name} - {self.variant.variant}'
class Coupon(models.Model):
    coupon_code=models.CharField(max_length=30)
    is_active=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=0)
    minimum_amount=models.IntegerField(default=500)
    applied=models.BooleanField(default=False)
    description = models.CharField(max_length=200,null=True,default='Sample')
    user=models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.coupon_code


class Banner(models.Model):
    name = models.CharField(max_length=30,default=None)
    image = models.ImageField(upload_to='imagestore/banner',default=None)
    def __str__(self):
        return self.name
    
class Wallet(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    

    def deposit(self, amount,type):
        self.balance += Decimal(str(amount))
        self.save()
        transaction = Transaction(wallet=self, amount=amount,type=type)
        transaction.save()

    def withdraw(self, amount,type):
        if self.balance >= amount:
            self.balance -= Decimal(str(amount))
            self.save()
            transaction = Transaction(wallet=self, amount=-amount,type=type)
            transaction.save()
        else:
            raise Exception("Insufficient balance")

    def transfer(self, amount, recipient_wallet):
        if self.balance >= amount:
            self.balance -= Decimal(str(amount))
            recipient_wallet.balance += Decimal(str(amount))
            self.save()
            recipient_wallet.save()
            transaction = Transaction(wallet=self, amount=-amount)
            transaction.save()
            transaction = Transaction(wallet=recipient_wallet, amount=amount)
            transaction.save()
        else:
            raise Exception("Insufficient balance")
    def get_transaction_history(self):
        return Transaction.objects.filter(wallet=self).order_by('-timestamp')
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=200,null=True,default='Transfer')
    def __str__(self):
        return f"Transaction ID: {self.id} | Wallet: {self.wallet} | Amount: {self.amount} | Timestamp: {self.timestamp} | Type:{self.type}"