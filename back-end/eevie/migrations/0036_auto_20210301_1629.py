# Generated by Django 3.1.4 on 2021-03-01 16:29

from django.db import migrations, models
import django.db.models.deletion
import eevie.validators


class Migration(migrations.Migration):

    dependencies = [
        ('eevie', '0035_auto_20210301_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='ac_charger',
        ),
        migrations.RemoveField(
            model_name='car',
            name='average_consumption',
        ),
        migrations.RemoveField(
            model_name='car',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='car',
            name='dc_charger',
        ),
        migrations.RemoveField(
            model_name='car',
            name='model',
        ),
        migrations.RemoveField(
            model_name='car',
            name='release_year',
        ),
        migrations.RemoveField(
            model_name='car',
            name='type',
        ),
        migrations.RemoveField(
            model_name='car',
            name='usable_battery_size',
        ),
        migrations.AlterField(
            model_name='car',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='CarBase',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=4, null=True)),
                ('model', models.CharField(max_length=100)),
                ('release_year', models.IntegerField(null=True, validators=[eevie.validators.validate_year])),
                ('usable_battery_size', models.FloatField(validators=[eevie.validators.validate_percentage])),
                ('average_consumption', models.FloatField(validators=[eevie.validators.validate_percentage])),
                ('ac_charger', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='eevie.accharger')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eevie.brands')),
                ('dc_charger', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='eevie.dccharger')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eevie.carbase'),
        ),
    ]