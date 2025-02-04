# Generated by Django 4.2.1 on 2025-01-22 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_master_gsp_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master_shopify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unq_id', models.CharField(max_length=255, verbose_name='UNQ_ID')),
                ('hinmei', models.CharField(max_length=255, verbose_name='商品名')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='カラー')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='サイズ')),
                ('sku', models.CharField(blank=True, max_length=255, null=True, verbose_name='SKU')),
                ('img_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='画像URL')),
            ],
        ),
    ]
