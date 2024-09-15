# Generated by Django 5.1.1 on 2024-09-11 17:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postfavorites',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='postfavorites',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique_favorite'),
        ),
    ]
