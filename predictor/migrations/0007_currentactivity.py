# Generated by Django 3.0.3 on 2020-02-05 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0006_auto_20200128_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_key', models.CharField(max_length=100)),
                ('activity', models.CharField(max_length=100)),
            ],
        ),
    ]
