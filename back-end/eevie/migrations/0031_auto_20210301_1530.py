# Generated by Django 3.1.4 on 2021-03-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eevie', '0030_auto_20210301_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='provider',
            field=models.ManyToManyField(related_name='sessions', to='eevie.Provider'),
        ),
    ]
