# Generated by Django 4.0.4 on 2022-05-12 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0005_alter_postfeed_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postuser', to=settings.AUTH_USER_MODEL)),
                ('postfeed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replys', to='feed.postfeed')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]