# Generated by Django 3.0.7 on 2021-01-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_investment_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='password_confirmation',
            field=models.CharField(default='', max_length=50),
        ),
    ]
