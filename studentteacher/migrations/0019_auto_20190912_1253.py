# Generated by Django 2.2.5 on 2019-09-12 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0018_auto_20190912_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='submission_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 12, 12, 53, 21, 789599)),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 9, 12, 12, 53, 21, 789627)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 9, 12, 12, 53, 21, 790246)),
        ),
    ]
