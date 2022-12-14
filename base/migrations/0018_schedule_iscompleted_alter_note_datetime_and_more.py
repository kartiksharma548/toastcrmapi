# Generated by Django 4.1 on 2022-10-06 08:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_status_status_id_name_alter_note_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='isCompleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='note',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 13, 58, 58, 462030)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='added_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 13, 58, 58, 462030)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 13, 58, 58, 462030)),
        ),
    ]
