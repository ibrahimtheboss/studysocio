# Generated by Django 4.0.4 on 2022-05-23 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studysocioprofile', '0010_alter_studysocioprofile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='studysocioprofile',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]
