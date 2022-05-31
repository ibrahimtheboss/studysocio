# Generated by Django 4.0.4 on 2022-05-22 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0002_alter_topic_options'),
        ('feed', '0008_alter_replyfeed_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='postfeed',
            name='topic',
            field=models.ForeignKey(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedtopic', to='topic.topic'),
        ),
    ]
