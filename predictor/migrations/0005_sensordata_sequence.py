# Generated by Django 3.0.2 on 2020-01-19 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0004_sensordata_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordata',
            name='sequence',
            field=models.CharField(default=-1, max_length=100),
            preserve_default=False,
        ),
    ]
