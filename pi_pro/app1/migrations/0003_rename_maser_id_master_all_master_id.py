# Generated by Django 4.2.1 on 2025-01-22 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_master_all_master_gsp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='master_all',
            old_name='maser_id',
            new_name='master_id',
        ),
    ]
