# Generated by Django 3.2.13 on 2022-06-18 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeclockapp', '0003_rename_clocktype_clock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clock',
            old_name='clocked_in',
            new_name='clockedIn',
        ),
        migrations.RenameField(
            model_name='clock',
            old_name='clocked_out',
            new_name='clockedOut',
        ),
    ]