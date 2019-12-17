# Generated by Django 3.0 on 2019-12-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.DecimalField(decimal_places=10, max_digits=30)),
                ('y', models.DecimalField(decimal_places=10, max_digits=30)),
                ('z', models.DecimalField(decimal_places=10, max_digits=30)),
                ('instant', models.DateField()),
            ],
        ),
    ]
