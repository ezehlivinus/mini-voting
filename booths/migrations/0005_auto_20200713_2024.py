# Generated by Django 3.0.1 on 2020-07-13 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booths', '0004_student_matric_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='poll',
        ),
        migrations.DeleteModel(
            name='Poll',
        ),
    ]
