# Generated by Django 3.2.7 on 2021-10-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionCargas', '0003_alter_remito_medio_pago'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistorialEstados',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]