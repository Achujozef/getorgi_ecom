# Generated by Django 4.1.7 on 2023-05-12 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('discount_price', models.IntegerField(default=0)),
                ('minimum_amount', models.IntegerField(default=500)),
                ('applied', models.BooleanField(default=False)),
                ('description', models.CharField(default='Sample', max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.userdetail')),
            ],
        ),
    ]
