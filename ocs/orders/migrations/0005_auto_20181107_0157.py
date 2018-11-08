# Generated by Django 2.1.2 on 2018-11-07 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20181107_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cantidad_productos',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orderproductinstatus',
            name='id_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.OrderProductStatus'),
        ),
        migrations.AlterField(
            model_name='orderproductstatus',
            name='descripcion',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='descripcion',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
