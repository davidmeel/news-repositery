# Generated by Django 5.1.1 on 2024-09-11 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_post_files_postfiles_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfiles',
            name='file',
            field=models.FileField(upload_to='files/'),
        ),
    ]
