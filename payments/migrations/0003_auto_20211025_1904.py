# Generated by Django 3.2.8 on 2021-10-25 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20211024_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='anticipated_amount',
            field=models.BooleanField(default=False, verbose_name='Valor antecipado'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='due_date',
            field=models.DateField(null=True, verbose_name='Data do vencimento'),
        ),
    ]