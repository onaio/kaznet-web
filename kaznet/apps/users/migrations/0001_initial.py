# Generated by Django 2.0.5 on 2018-05-28 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
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
                     blank=True,
                     db_index=True,
                     default=None,
                     null=True,
                     unique=True,
                     verbose_name='Ona Primary key')),
                ('ona_username',
                 models.CharField(
                     blank=True,
                     db_index=True,
                     default=None,
                     max_length=255,
                     null=True,
                     unique=True,
                     verbose_name='Ona Username')),
                ('national_id',
                 models.CharField(
                     blank=True,
                     db_index=True,
                     default=None,
                     max_length=255,
                     null=True,
                     unique=True,
                     verbose_name='National ID Number')),
                ('mpesa_number',
                 phonenumber_field.modelfields.PhoneNumberField(
                     blank=True,
                     default='',
                     max_length=128,
                     verbose_name='MPESA number')),
                ('phone_number',
                 phonenumber_field.modelfields.PhoneNumberField(
                     blank=True,
                     default='',
                     max_length=128,
                     verbose_name='Phone number')),
                ('role',
                 models.CharField(
                     blank=True,
                     choices=[('1', 'Admin'), ('2', 'Contributor')],
                     default='2',
                     max_length=1,
                     verbose_name='Role')),
                ('expertise',
                 models.CharField(
                     blank=True,
                     choices=[('1', 'Beginner'), ('2', 'Intermediate'),
                              ('3', 'Advanced'), ('4', 'Expert')],
                     default='1',
                     max_length=1,
                     verbose_name='Expertise')),
                ('gender',
                 models.CharField(
                     blank=True,
                     choices=[('0', 'Other'), ('1', 'Male'), ('2', 'Female')],
                     default='0',
                     max_length=1,
                     verbose_name='Gender')),
                ('user',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL,
                     verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
