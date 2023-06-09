# Generated by Django 4.1.7 on 2023-05-12 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=12)),
                ('housename', models.CharField(max_length=50)),
                ('locality', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(choices=[('KARNATAKA', 'KARNATAKA'), ('KERALA', 'KERALA'), ('TAMIL NADU', 'TAMIL NADU'), ('GOA', 'GOA'), ('GUJARAT', 'GUJARAT')], default='KERALA', max_length=50)),
                ('selected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cartid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MyAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupen', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=50)),
                ('discount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default='', max_length=200)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('normalprice', models.IntegerField(default=0)),
                ('listed', models.BooleanField(default=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopping.category')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=50, unique=True)),
                ('uemail', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('upassword', models.CharField(max_length=50)),
                ('uactive', models.BooleanField(default=True)),
                ('uimage', models.ImageField(blank=True, null=True, upload_to='imagestore/')),
                ('uotp', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shopping.userdetail')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('stock', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.variant')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(through='shopping.ProductVariant', to='shopping.variant'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('ordertype', models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('Paypal', 'Paypal'), ('Razorpay', 'Razorpay')], default='Cash on delivery', max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On the way', 'On the way'), ('Delivered', 'Delivered'), ('Cancel Requested', 'Cancel Requested'), ('Return Requested', 'Return Requested'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Pending', max_length=50)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.address')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.userdetail')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shopping.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('cartitemid', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveBigIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.userdetail'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.userdetail'),
        ),
    ]
