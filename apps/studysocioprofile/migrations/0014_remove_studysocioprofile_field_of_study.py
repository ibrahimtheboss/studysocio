# Generated by Django 4.0.4 on 2022-06-07 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studysocioprofile', '0013_studysocioprofile_background_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studysocioprofile',
            name='field_of_study',
        ),
    ]