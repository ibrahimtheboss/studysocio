# Generated by Django 4.0.4 on 2022-04-26 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupconversation', '0009_delete_groupconversationmembers'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupConversationMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('groupconversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groupconversation.groupconversation')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
