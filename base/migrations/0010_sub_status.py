# Generated by Django 4.1 on 2022-09-21 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_lead_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub_Status',
            fields=[
                ('sub_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_status_name', models.CharField(default='', max_length=64)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.status')),
            ],
        ),
    ]