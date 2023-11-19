from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Sensor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    sensor_id = models.PositiveIntegerField()


class SensorSample(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    sampled_at = models.DateTimeField(default=timezone.now)
    data = models.TextField()
