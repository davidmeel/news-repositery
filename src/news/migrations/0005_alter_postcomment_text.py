# Generated by Django 5.1.1 on 2024-09-15 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_postfiles_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='text',
            field=models.CharField(max_length=48),
        ),
    ]
