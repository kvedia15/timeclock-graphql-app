# Generated by Django 3.2.13 on 2022-06-18 04:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timeclockapp', '0002_auto_20220618_0436'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='clockType',
            new_name='Clock',
        ),
    ]
