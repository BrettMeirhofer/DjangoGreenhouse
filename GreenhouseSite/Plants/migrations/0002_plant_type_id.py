# Generated by Django 4.0.1 on 2022-01-29 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='type_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]