# Generated by Django 2.2.1 on 2020-05-08 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tezpay', '0006_auto_20200508_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipts',
            name='market',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tezpay.Market'),
        ),
    ]
