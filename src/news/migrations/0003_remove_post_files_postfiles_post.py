# Generated by Django 5.1.1 on 2024-09-11 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_postfavorites_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='files',
        ),
        migrations.AddField(
            model_name='postfiles',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='news.post'),
            preserve_default=False,
        ),
    ]
