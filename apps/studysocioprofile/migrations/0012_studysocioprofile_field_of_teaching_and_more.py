# Generated by Django 4.0.4 on 2022-05-29 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studysocioprofile', '0011_studysocioprofile_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='studysocioprofile',
            name='field_of_teaching',
            field=models.CharField(blank=True, default=' ', max_length=300),
        ),
        migrations.AlterField(
            model_name='studysocioprofile',
            name='education_center',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='studysocioprofile',
            name='field_of_study',
            field=models.CharField(blank=True, default=' ', max_length=300),
        ),
    ]