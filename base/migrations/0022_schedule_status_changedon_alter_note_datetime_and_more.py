# Generated by Django 4.1 on 2022-10-13 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_schedule_schedule_updatedatetime_alter_note_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='status_changedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 14, 51, 16, 280943)),
        ),
        migrations.AlterField(
            model_name='note',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 14, 51, 16, 279943)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='added_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 14, 51, 16, 280943)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 14, 51, 16, 280943)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_updatedateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 14, 51, 16, 280943)),
        ),
    ]