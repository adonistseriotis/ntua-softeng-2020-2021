# Generated by Django 3.1.4 on 2021-02-03 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eevie', '0006_auto_20210203_1739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accharger',
            old_name='idd',
            new_name='id',
        ),
    ]
