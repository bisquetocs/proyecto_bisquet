# Generated by Django 2.1.2 on 2018-11-04 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20181103_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkedinventory',
            name='id_franchise',
        ),
        migrations.RemoveField(
            model_name='linkedinventory',
            name='id_product',
        ),
        migrations.DeleteModel(
            name='LinkedInventory',
        ),
    ]
