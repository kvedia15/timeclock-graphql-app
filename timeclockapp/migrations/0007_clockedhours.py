# Generated by Django 3.2.13 on 2022-06-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeclockapp', '0006_rename_clock_clockitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClockedHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('today', models.IntegerField(null=True)),
                ('currentWeek', models.IntegerField(null=True)),
                ('currentMonth', models.IntegerField(null=True)),
            ],
        ),
    ]
