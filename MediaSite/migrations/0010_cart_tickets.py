# Generated by Django 4.2 on 2024-05-17 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediaSite', '0009_remove_ticket_user_cart_ticket_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tickets',
            field=models.ManyToManyField(related_name='carts', to='MediaSite.ticket'),
        ),
    ]
