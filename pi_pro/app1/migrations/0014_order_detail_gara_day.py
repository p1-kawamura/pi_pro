# Generated by Django 4.2.1 on 2025-01-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_order_detail_body_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='gara_day',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='柄名_使用日'),
        ),
    ]
