# Generated by Django 2.2.5 on 2019-09-20 08:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0050_auto_20190920_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 20, 8, 8, 28, 874155)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 20, 8, 8, 28, 874760)),
        ),
    ]