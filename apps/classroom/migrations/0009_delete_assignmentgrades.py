# Generated by Django 4.0.4 on 2022-05-16 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_lessonmaterials_total_marks_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AssignmentGrades',
        ),
    ]