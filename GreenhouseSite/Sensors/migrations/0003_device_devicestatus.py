# Generated by Django 4.0.1 on 2022-01-18 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sensors', '0002_alter_reading_sensor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('status_datetime', models.DateTimeField()),
                ('device', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='Sensors.device')),
            ],
        ),
    ]
