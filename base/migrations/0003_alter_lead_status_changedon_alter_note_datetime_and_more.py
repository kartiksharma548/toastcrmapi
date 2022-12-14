# Generated by Django 4.1 on 2022-10-17 18:34

import datetime
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_lead_status_changedon_alter_note_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='status_changedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 0, 4, 40, 124770)),
        ),
        migrations.AlterField(
            model_name='note',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 0, 4, 40, 124770)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='added_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 0, 4, 40, 125770)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 0, 4, 40, 125770)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_updatedateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 0, 4, 40, 125770)),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=django_resized.forms.ResizedImageField(crop=None, default='', force_format=None, keep_meta=True, quality=-1, scale=None, size=[210, 240], upload_to='images'),
        ),
    ]
