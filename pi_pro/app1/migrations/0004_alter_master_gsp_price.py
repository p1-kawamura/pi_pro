# Generated by Django 4.2.1 on 2025-01-22 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_maser_id_master_all_master_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_gsp',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='原価'),
        ),
    ]
