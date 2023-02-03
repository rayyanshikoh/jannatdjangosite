# Generated by Django 4.1 on 2023-02-01 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_clear_date_product_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='payment_status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P', max_length=1),
        ),
    ]
