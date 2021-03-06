# Generated by Django 2.2.5 on 2019-09-18 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0046_auto_20190917_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 18, 5, 50, 15, 816704)),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 18, 5, 50, 15, 817350)),
        ),
    ]
