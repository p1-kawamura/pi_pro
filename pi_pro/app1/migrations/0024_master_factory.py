# Generated by Django 4.2.1 on 2025-02-14 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_master_gsp_factory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master_factory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factroy', models.CharField(blank=True, max_length=255, null=True, verbose_name='GSP_商品コード')),
            ],
        ),
    ]
