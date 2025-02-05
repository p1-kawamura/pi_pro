# Generated by Django 4.2.1 on 2025-02-05 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_order_list_ship_limit_alter_order_list_ship_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_gsp',
            name='sender_adress1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り主_番地'),
        ),
        migrations.AlterField(
            model_name='master_gsp',
            name='sender_city',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り主_市区町村'),
        ),
        migrations.AlterField(
            model_name='master_gsp',
            name='sender_com',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り主_会社'),
        ),
        migrations.AlterField(
            model_name='master_gsp',
            name='sender_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り主_氏名'),
        ),
        migrations.AlterField(
            model_name='master_gsp',
            name='sender_pref',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り主_都道府県'),
        ),
        migrations.AlterField(
            model_name='master_gsp',
            name='sender_tel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り主_電話番号'),
        ),
        migrations.AlterField(
            model_name='master_gsp',
            name='sender_yubin',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='送り主_郵便番号'),
        ),
    ]
