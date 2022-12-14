# Generated by Django 4.1 on 2022-10-12 19:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_sub_status_statusforcancellation_alter_note_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='schedule_updatedateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 0, 48, 28, 110100)),
        ),
        migrations.AlterField(
            model_name='note',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 0, 48, 28, 110100)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='added_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 0, 48, 28, 110100)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 13, 0, 48, 28, 110100)),
        ),
        migrations.AlterField(
            model_name='sub_status',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='status_field', to='base.status'),
        ),
    ]
