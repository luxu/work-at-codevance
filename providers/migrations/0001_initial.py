# Generated by Django 3.2.8 on 2021-10-24 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Providers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=14)),
                ('corporate_name', models.CharField(blank=True, max_length=30, verbose_name='Razão Social')),
            ],
        ),
    ]