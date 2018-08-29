# Generated by Django 2.0.7 on 2018-08-29 08:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gravatar',
            field=models.URLField(
                blank=True,
                default=None,
                null=True,
                verbose_name='Gravatar Link'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True, default=dict, verbose_name='Metadata'),
        ),
    ]
