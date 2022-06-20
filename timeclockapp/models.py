from dataclasses import asdict
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ClockItem(models.Model):
    user = models.ForeignKey(User, related_name="timeclockapp", on_delete=models.CASCADE)
    clockIn = models.DateTimeField(null=True,blank=True)
    clockOut = models.DateTimeField(null=True,blank=True)

class ClockedHours(models.Model):
    today=models.IntegerField(null=True,blank=False)
    currentWeek=models.IntegerField(null=True,blank=False)
    currentMonth=models.IntegerField(null=True,blank=False)