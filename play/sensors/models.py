import json
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
import requests


class Sensor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    sensor_id = models.PositiveIntegerField()

    def __str__(self):
        return f'Sensor({self.id}, sensor_id={self.sensor_id})'

    @classmethod
    def sample(cls, sensor):
        read_key = os.getenv('PURPLEAIR_READ_KEY')
        if read_key is None:
            j = {'error': 'No PURPLEAIR_READ_KEY in .env'}
        else:
            headers = {
                "X-API-Key": read_key,
            }
            url = f'https://api.purpleair.com/v1/sensors/{sensor.sensor_id}'
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                j = {'error': r.status_code() }
            else:
                # There's an opportunity here to remove cruft
                j = r.json()

        sample = SensorSample(sensor=sensor, data=json.dumps(j))
        sample.save()


class SensorSample(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    sampled_at = models.DateTimeField(default=timezone.now)
    data = models.TextField()

    @property
    def temp_f(self):
        j = json.loads(self.data)
        if 'error' in j.keys():
            return mark_safe(
                f'<span style="color: red">{j["error"]}</span>')

        temp = j['sensor']['temperature']
        return mark_safe(
            f'<span style="color: green">{temp}&deg;</span>')

    def __str__(self):
        return f'SensorSample({self.id}, sensor_id={self.sensor.sensor_id}, at {self.sampled_at})'
