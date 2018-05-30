# Generated by Django 2.0.5 on 2018-05-30 07:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='OnaInstance',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('created',
                 models.DateTimeField(
                     auto_now_add=True, verbose_name='Created')),
                ('modified',
                 models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('ona_pk',
                 models.PositiveIntegerField(
                     db_index=True,
                     unique=True,
                     verbose_name='Onadata Primary Key')),
                ('json',
                 django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('deleted_at',
                 models.DateTimeField(
                     default=None, null=True, verbose_name='Deleted at')),
                ('ona_last_updated',
                 models.DateTimeField(
                     blank=True,
                     default=None,
                     null=True,
                     verbose_name='Last Updated on Ona')),
                ('edited',
                 models.BooleanField(
                     default=False,
                     help_text=
                     'This represents whether the submission has been edited',
                     verbose_name='Edited')),
            ],
            options={
                'ordering': ['ona_pk', 'deleted_at'],
            },
        ),
        migrations.CreateModel(
            name='OnaProject',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('created',
                 models.DateTimeField(
                     auto_now_add=True, verbose_name='Created')),
                ('modified',
                 models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('ona_pk',
                 models.PositiveIntegerField(
                     db_index=True,
                     unique=True,
                     verbose_name='Onadata Primary Key')),
                ('ona_organization',
                 models.PositiveIntegerField(
                     blank=True,
                     default=None,
                     null=True,
                     verbose_name='Onadata Organization ID')),
                ('name', models.CharField(max_length=255)),
                ('deleted_at',
                 models.DateTimeField(
                     default=None, null=True, verbose_name='Deleted at')),
                ('ona_last_updated',
                 models.DateTimeField(verbose_name='Last Updated on Ona')),
            ],
            options={
                'ordering': ['name', 'ona_pk'],
            },
        ),
        migrations.CreateModel(
            name='XForm',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('created',
                 models.DateTimeField(
                     auto_now_add=True, verbose_name='Created')),
                ('modified',
                 models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('ona_pk',
                 models.PositiveIntegerField(
                     db_index=True,
                     unique=True,
                     verbose_name='Onadata Primary Key')),
                ('ona_project_id',
                 models.PositiveIntegerField(
                     db_index=True, verbose_name='Onadata project ID')),
                ('title',
                 models.CharField(
                     editable=False, max_length=255, verbose_name='Title')),
                ('id_string',
                 models.SlugField(
                     editable=False, max_length=100,
                     verbose_name='ID String')),
                ('deleted_at',
                 models.DateTimeField(
                     default=None, null=True, verbose_name='Deleted at')),
            ],
            options={
                'ordering': ['title', 'id_string'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='xform',
            unique_together={('ona_project_id', 'id_string')},
        ),
        migrations.AddField(
            model_name='onainstance',
            name='xform',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='ona.XForm'),
        ),
    ]
