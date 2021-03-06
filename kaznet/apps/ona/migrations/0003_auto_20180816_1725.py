# Generated by Django 2.0.7 on 2018-08-16 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ona', '0002_auto_20180720_1344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='xform',
            old_name='project_id',
            new_name='ona_project_id',
        ),
        migrations.AddField(
            model_name='xform',
            name='project',
            field=models.ForeignKey(blank=True, db_column='project_custom', help_text='This references the Kaznet Project.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ona.Project', verbose_name='Kaznet Project'),
        ),
        migrations.AlterUniqueTogether(
            name='xform',
            unique_together={('ona_project_id', 'id_string')},
        ),
    ]
