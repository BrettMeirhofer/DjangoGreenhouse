# Generated by Django 4.0.2 on 2022-03-31 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plants', '0005_plant_clone_plant_parent1_plant_parent2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='planter_capacity',
            field=models.FloatField(default=0),
        ),
    ]