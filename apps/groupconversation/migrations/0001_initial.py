# Generated by Django 4.0.4 on 2022-04-25 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupConversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('groupimage', models.ImageField(blank=True, null=True, upload_to='group_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('users', models.ManyToManyField(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-modified_at'],
            },
        ),
        migrations.CreateModel(
            name='GroupConversationMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='groupconversation_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupmessages', to=settings.AUTH_USER_MODEL)),
                ('groupconversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupmessages', to='groupconversation.groupconversation')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
