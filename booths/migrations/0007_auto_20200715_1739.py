# Generated by Django 3.0.1 on 2020-07-15 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booths', '0006_choice_number_of_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avater',
            field=models.FileField(blank=True, null=True, upload_to=None, verbose_name='passport'),
        ),
    ]
