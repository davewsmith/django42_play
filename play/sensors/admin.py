from django.contrib import admin
from .models import Sensor, SensorSample


admin.site.register(Sensor)
admin.site.register(SensorSample)
