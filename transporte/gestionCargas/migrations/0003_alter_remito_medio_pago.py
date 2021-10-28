# Generated by Django 3.2.7 on 2021-09-30 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCargas', '0002_alter_estadoremito_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remito',
            name='medio_pago',
            field=models.CharField(choices=[('OR', 'Pago en Origen'), ('DES', 'Pago en Destino'), ('CC', 'Pago con Cuenta Corriente')], max_length=20, null=True),
        ),
    ]
