# Generated by Django 3.2.8 on 2021-10-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_order_given_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost_of_given_product',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Стоимость'),
        ),
    ]