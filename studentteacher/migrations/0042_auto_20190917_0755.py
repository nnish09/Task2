# Generated by Django 2.2.5 on 2019-09-17 07:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0041_auto_20190917_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 7, 55, 9, 271289)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 7, 55, 9, 271958)),
        ),
    ]
