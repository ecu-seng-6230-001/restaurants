# Generated by Django 3.1.2 on 2020-11-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('pod', 'Pay On Delivery'), ('paypal', 'PayPal')], default='pod', max_length=100),
        ),
    ]
