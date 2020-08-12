# Generated by Django 3.0.8 on 2020-08-11 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20200808_0906'),
        ('order', '0002_auto_20200811_1549'),
        ('user', '0002_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='order_item',
            field=models.ManyToManyField(through='order.Order', to='product.Product'),
        ),
    ]
