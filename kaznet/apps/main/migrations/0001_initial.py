# Generated by Django 2.0.7 on 2018-07-05 13:16

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import django_prices.models
import mptt.fields
import tasking.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bounty',
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
                ('amount',
                 django_prices.models.MoneyField(
                     currency='KES',
                     decimal_places=2,
                     default=0,
                     max_digits=64,
                     verbose_name='Amount')),
            ],
            options={
                'verbose_name': 'Bounty',
                'verbose_name_plural': 'Bounties',
                'ordering': ['created', 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
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
                ('name',
                 models.CharField(
                     help_text='Name of the client.',
                     max_length=255,
                     verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['id', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
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
                ('name',
                 models.CharField(
                     help_text='This represents the name of Location.',
                     max_length=255,
                     verbose_name='Name')),
                ('country',
                 django_countries.fields.CountryField(
                     blank=True,
                     default='',
                     help_text='This represents the Country.',
                     max_length=2,
                     verbose_name='Country')),
                ('geopoint',
                 django.contrib.gis.db.models.fields.PointField(
                     blank=True,
                     default=None,
                     help_text=
                     'This represents the Geographical Point of the Location.',
                     null=True,
                     srid=4326,
                     verbose_name='GeoPoint')),
                ('radius',
                 models.DecimalField(
                     blank=True,
                     decimal_places=4,
                     default=None,
                     help_text='This represents the radius from the geopoint.',
                     max_digits=64,
                     null=True,
                     verbose_name='Radius')),
                ('shapefile',
                 django.contrib.gis.db.models.fields.MultiPolygonField(
                     blank=True,
                     default=None,
                     help_text='This represents the Shapefile of the Location',
                     null=True,
                     srid=4326,
                     verbose_name='Shapefile')),
                ('description',
                 models.TextField(
                     blank=True,
                     default='',
                     help_text=
                     'This represents the description of the Location.',
                     verbose_name='Description')),
                ('lft',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('level',
                 models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'ordering': ['country', 'name', 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocationType',
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
                ('name',
                 models.CharField(
                     help_text='This is the name of the Location Type',
                     max_length=255,
                     verbose_name='Name')),
            ],
            options={
                'ordering': ['name', 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
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
                ('target_object_id',
                 models.PositiveIntegerField(
                     blank=True, db_index=True, default=None, null=True)),
                ('name',
                 models.CharField(
                     help_text='This is the name of the Project',
                     max_length=255,
                     verbose_name='Name')),
                ('target_content_type',
                 models.ForeignKey(
                     blank=True,
                     default=None,
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SegmentRule',
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
                ('name',
                 models.CharField(
                     help_text='The name of this rule.',
                     max_length=255,
                     verbose_name='Name')),
                ('description',
                 models.TextField(
                     blank=True,
                     default='',
                     help_text='The description of this rule.',
                     verbose_name='Description')),
                ('target_field',
                 models.CharField(
                     db_index=True,
                     help_text='The field on the target model.',
                     max_length=255,
                     verbose_name='Target Field')),
                ('target_field_value',
                 models.CharField(
                     help_text='The value of the target field',
                     max_length=255,
                     verbose_name='Target Field Value')),
                ('active', models.BooleanField()),
                ('target_content_type',
                 models.ForeignKey(
                     blank=True,
                     default=None,
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     related_name='segment_rule',
                     to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Submission',
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
                ('target_object_id',
                 models.PositiveIntegerField(
                     blank=True, db_index=True, default=None, null=True)),
                ('submission_time',
                 models.DateTimeField(
                     help_text=
                     'This is the date and time the task was submitted.',
                     verbose_name='Submission Time')),
                ('valid',
                 models.BooleanField(
                     default=False,
                     help_text=
                     'This represents whether submission is valid or not.',
                     verbose_name='Valid')),
                ('status',
                 models.CharField(
                     choices=[('a', 'Approved'), ('b', 'Rejected'),
                              ('c', 'Under Review'), ('d', 'Pending Review')],
                     default='d',
                     help_text='The status of the Submission',
                     max_length=1,
                     verbose_name='Status')),
                ('comments',
                 models.TextField(
                     blank=True,
                     default='',
                     help_text='This represents the comments.',
                     verbose_name='Comments')),
                ('bounty',
                 models.ForeignKey(
                     help_text='This represents the Bounty.',
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     to='main.Bounty',
                     verbose_name='Bounty')),
                ('location',
                 models.ForeignKey(
                     blank=True,
                     default=None,
                     help_text='This represents the Location.',
                     null=True,
                     on_delete=django.db.models.deletion.PROTECT,
                     to='main.Location',
                     verbose_name='Location')),
                ('target_content_type',
                 models.ForeignKey(
                     blank=True,
                     default=None,
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['submission_time', 'task__name', 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
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
                ('target_object_id',
                 models.PositiveIntegerField(
                     blank=True, db_index=True, default=None, null=True)),
                ('name',
                 models.CharField(
                     help_text='This represents the name.',
                     max_length=255,
                     verbose_name='Name')),
                ('description',
                 models.TextField(
                     blank=True,
                     default='',
                     help_text='This represents the description.',
                     verbose_name='Description')),
                ('start',
                 models.DateTimeField(
                     help_text='This is the date and time the task starts.',
                     verbose_name='Start')),
                ('end',
                 models.DateTimeField(
                     blank=True,
                     default=None,
                     help_text='This is the date and time the task ends.',
                     null=True,
                     verbose_name='End')),
                ('timing_rule',
                 models.TextField(
                     blank=True,
                     default=None,
                     help_text='This stores the rrule for recurrence.',
                     null=True,
                     validators=[tasking.validators.validate_rrule],
                     verbose_name='Timing Rule')),
                ('total_submission_target',
                 models.IntegerField(
                     blank=True,
                     default=None,
                     help_text=
                     'This is the total number of submissions required for this task. Set to None if there is no Max.',
                     null=True,
                     verbose_name='Total Submissions Target')),
                ('user_submission_target',
                 models.IntegerField(
                     blank=True,
                     default=None,
                     help_text=
                     'This is the total number of submissions per user required for this task. Set to None if there is no Max.',
                     null=True,
                     verbose_name='User Submissions Target')),
                ('status',
                 models.CharField(
                     choices=[('a', 'Active'), ('b', 'Deactivated'),
                              ('c', 'Expired'), ('d', 'Draft'),
                              ('s', 'Scheduled'), ('e', 'Archived')],
                     default='d',
                     help_text='The status of the Task',
                     max_length=1,
                     verbose_name='Status')),
                ('estimated_time',
                 models.DurationField(
                     blank=True,
                     default=None,
                     help_text=
                     'This represents the estimated time it takes to complete a task',
                     null=True,
                     verbose_name='Estimated Time')),
                ('required_expertise',
                 models.CharField(
                     blank=True,
                     choices=[('1', 'Beginner'), ('2', 'Intermediate'),
                              ('3', 'Advanced'), ('4', 'Expert')],
                     default='1',
                     max_length=1,
                     verbose_name='Recommended Expertise')),
                ('lft',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('level',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('client',
                 models.ForeignKey(
                     blank=True,
                     default=None,
                     help_text='This represents the client.',
                     null=True,
                     on_delete=django.db.models.deletion.SET_NULL,
                     to='main.Client',
                     verbose_name='Client')),
            ],
            options={
                'ordering': ['start', 'name', 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskLocation',
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
                ('timing_rule',
                 models.TextField(
                     help_text='This stores the rrule for recurrence.',
                     validators=[tasking.validators.validate_rrule],
                     verbose_name='Timing Rule')),
                ('start', models.TimeField(verbose_name='Start Time')),
                ('end', models.TimeField(verbose_name='End Time')),
                ('location',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='main.Location')),
                ('task',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='main.Task')),
            ],
            options={
                'ordering': ['task', 'location', 'start'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskOccurrence',
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
                ('date',
                 models.DateField(
                     help_text='The date of the occurrence',
                     verbose_name='Date')),
                ('start_time',
                 models.TimeField(
                     help_text='The start time of the occurrence',
                     verbose_name='Start Time')),
                ('end_time',
                 models.TimeField(
                     help_text='The end time of the occurrence',
                     verbose_name='End Time')),
                ('task',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='main.Task',
                     verbose_name='Task Occurrence')),
            ],
            options={
                'ordering': ['task', 'date', 'start_time'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='locations',
            field=models.ManyToManyField(
                blank=True,
                default=None,
                help_text='This represents the locations.',
                through='main.TaskLocation',
                to='main.Location',
                verbose_name='Locations'),
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True,
                default=None,
                help_text='This represents the parent task.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='main.Task',
                verbose_name='Parent task'),
        ),
        migrations.AddField(
            model_name='task',
            name='segment_rules',
            field=models.ManyToManyField(
                blank=True,
                default=None,
                to='main.SegmentRule',
                verbose_name='Segment Rules'),
        ),
        migrations.AddField(
            model_name='task',
            name='target_content_type',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='submission',
            name='task',
            field=models.ForeignKey(
                help_text='This represents the Task.',
                on_delete=django.db.models.deletion.PROTECT,
                to='main.Task',
                verbose_name='Task'),
        ),
        migrations.AddField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(
                help_text='This represents the User.',
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name='User'),
        ),
        migrations.AddField(
            model_name='project',
            name='tasks',
            field=models.ManyToManyField(
                blank=True,
                default=None,
                help_text='This represents the Task.',
                to='main.Task',
                verbose_name='Tasks'),
        ),
        migrations.AddField(
            model_name='location',
            name='location_type',
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text='This represents the Location Type',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='main.LocationType',
                verbose_name='Location Type'),
        ),
        migrations.AddField(
            model_name='location',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='children',
                to='main.Location'),
        ),
        migrations.AddField(
            model_name='bounty',
            name='task',
            field=models.ForeignKey(
                help_text='The task the bounty is for.',
                on_delete=django.db.models.deletion.CASCADE,
                to='main.Task',
                verbose_name='Task'),
        ),
    ]
