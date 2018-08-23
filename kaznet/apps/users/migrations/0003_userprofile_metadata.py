# Generated by Django 2.0.7 on 2018-08-21 13:08

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
