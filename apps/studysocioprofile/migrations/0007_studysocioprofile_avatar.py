# Generated by Django 4.0.4 on 2022-04-18 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studysocioprofile', '0006_followrequest_alter_studysocioprofile_follows_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studysocioprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
