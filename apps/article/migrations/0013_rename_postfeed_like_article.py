# Generated by Django 4.0.4 on 2022-05-27 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_alter_article_options_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='PostFeed',
            new_name='Article',
        ),
    ]
