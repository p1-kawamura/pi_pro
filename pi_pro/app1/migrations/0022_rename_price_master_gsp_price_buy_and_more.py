# Generated by Django 4.2.1 on 2025-02-07 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_order_detail_shi_bikou_order_detail_shi_factory_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='master_gsp',
            old_name='price',
            new_name='price_buy',
        ),
        migrations.RenameField(
            model_name='order_detail',
            old_name='genka',
            new_name='price_buy',
        ),
        migrations.RemoveField(
            model_name='order_detail',
            name='tanka',
        ),
        migrations.AddField(
            model_name='master_gsp',
            name='price_sell',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='請求単価'),
        ),
        migrations.AddField(
            model_name='order_detail',
            name='price_last',
            field=models.IntegerField(blank=True, null=True, verbose_name='エンドユーザー単価'),
        ),
        migrations.AddField(
            model_name='order_detail',
            name='price_sell',
            field=models.IntegerField(blank=True, null=True, verbose_name='請求単価'),
        ),
    ]
