# Generated by Django 2.2.5 on 2019-09-11 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0011_auto_20190911_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
