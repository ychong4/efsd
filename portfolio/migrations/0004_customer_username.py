# Generated by Django 3.0.7 on 2021-01-23 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20210123_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(default='', max_length=50),
        ),
    ]
