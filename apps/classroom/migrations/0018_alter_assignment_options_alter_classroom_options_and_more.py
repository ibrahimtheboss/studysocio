# Generated by Django 4.0.4 on 2022-05-28 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0017_remove_assignmentgrades_status_assignment_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['-modified_at']},
        ),
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ['-modified_at']},
        ),
        migrations.AlterModelOptions(
            name='lessonmaterials',
            options={'ordering': ['-modified_at']},
        ),
    ]