# Generated by Django 4.2.1 on 2025-02-25 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0026_rename_factroy_factory_factory'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='body_check',
            field=models.IntegerField(default=0, verbose_name='ボディ発注CSV'),
        ),
        migrations.AddField(
            model_name='order_detail',
            name='shiji_check',
            field=models.IntegerField(default=0, verbose_name='指示書CSV'),
        ),
        migrations.AddField(
            model_name='order_detail',
            name='ship_check',
            field=models.IntegerField(default=0, verbose_name='出荷CSV'),
        ),
    ]
