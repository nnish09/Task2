# Generated by Django 2.2.5 on 2019-09-20 08:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0051_auto_20190920_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 20, 8, 9, 34, 924026)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 20, 8, 9, 34, 924650)),
        ),
    ]
