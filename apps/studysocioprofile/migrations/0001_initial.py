# Generated by Django 4.0.4 on 2022-04-11 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudySocioProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=250)),
                ('field_of_study', models.CharField(blank=True, max_length=40)),
                ('education_center', models.CharField(max_length=60)),
                ('designation', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], max_length=7)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('follows', models.ManyToManyField(related_name='followed_by', to='studysocioprofile.studysocioprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
