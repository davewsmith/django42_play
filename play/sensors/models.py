from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Sensor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    sensor_id = models.PositiveIntegerField()

    def __str__(self):
        return f'Sensor({self.id}, sensor_id={self.sensor_id})'

    @classmethod
    def sample(cls, sensor):
        sample = SensorSample(sensor=sensor, data='Still fake')
        sample.save()

class SensorSample(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    sampled_at = models.DateTimeField(default=timezone.now)
    data = models.TextField()

    def __str__(self):
        return f'SensorSample({self.id}, sensor_id={self.sensor.sensor_id}, at {self.sampled_at})'
