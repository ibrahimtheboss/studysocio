# Generated by Django 4.0.4 on 2022-04-26 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupconversation', '0008_remove_groupconversationmembers_added_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GroupConversationMembers',
        ),
    ]
