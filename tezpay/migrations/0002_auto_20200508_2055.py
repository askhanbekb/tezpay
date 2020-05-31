# Generated by Django 2.2.1 on 2020-05-08 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tezpay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=555, null=True)),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payed', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], max_length=555, null=True)),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.CreateModel(
            name='ShopType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=555, null=True)),
            ],
            options={
                'verbose_name': 'Тип покупки',
                'verbose_name_plural': 'Тип покупки',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=555, null=True)),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='receipts',
            options={'verbose_name': 'Чек', 'verbose_name_plural': 'Чек'},
        ),
        migrations.RemoveField(
            model_name='receipts',
            name='products',
        ),
        migrations.RemoveField(
            model_name='receipts',
            name='title',
        ),
        migrations.AddField(
            model_name='products',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='products',
            name='description',
            field=models.CharField(blank=True, max_length=555, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.CharField(max_length=555, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='receipts',
            name='receipt_id',
            field=models.CharField(default=uuid.uuid4, max_length=555, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tezpay.Category'),
        ),
        migrations.DeleteModel(
            name='ReceiptProduct',
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tezpay.Products'),
        ),
        migrations.AddField(
            model_name='orders',
            name='receipt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tezpay.Receipts'),
        ),
        migrations.AddField(
            model_name='orders',
            name='shop_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tezpay.ShopType'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='products',
            name='market',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tezpay.Market'),
        ),
        migrations.AddField(
            model_name='products',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tezpay.Status'),
        ),
    ]
