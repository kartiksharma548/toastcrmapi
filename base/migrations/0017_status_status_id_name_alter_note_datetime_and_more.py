# Generated by Django 4.1 on 2022-10-02 06:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_allowedstatus_current_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='status_id_name',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='note',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 2, 12, 17, 6, 691678)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='added_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 2, 12, 17, 6, 691678)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 2, 12, 17, 6, 691678)),
        ),
    ]
