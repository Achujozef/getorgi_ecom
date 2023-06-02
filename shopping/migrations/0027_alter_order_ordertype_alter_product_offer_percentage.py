# Generated by Django 4.1.7 on 2023-06-02 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0026_rename_price_befor_offer_productvariant_price_after_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordertype',
            field=models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('Online Payment', 'Online Payment'), ('Razorpay', 'Razorpay'), ('Wallet', 'Wallet')], default='Cash on delivery', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='offer_percentage',
            field=models.IntegerField(default=0),
        ),
    ]
