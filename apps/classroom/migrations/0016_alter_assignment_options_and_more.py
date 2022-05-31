# Generated by Django 4.0.4 on 2022-05-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0015_alter_classroom_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['modified_at']},
        ),
        migrations.AlterModelOptions(
            name='lessonmaterials',
            options={'ordering': ['modified_at']},
        ),
        migrations.AddField(
            model_name='assignmentgrades',
            name='status',
            field=models.CharField(blank=True, choices=[('Available', 'Available'), ('Due', 'Due')], default='Available', max_length=10),
        ),
    ]