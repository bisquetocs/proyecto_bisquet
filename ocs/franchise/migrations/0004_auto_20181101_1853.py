# Generated by Django 2.1.2 on 2018-11-02 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('franchise', '0003_privateproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privateproduct',
            name='id_franchise',
        ),
        migrations.DeleteModel(
            name='PrivateProduct',
        ),
    ]
