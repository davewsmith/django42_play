from django.contrib import admin
from .models import Sensor, SensorSample


class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sensor_id', 'created')
    read_only = ('id', 'user', 'created')

admin.site.register(Sensor, SensorAdmin)


class SensorSampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sampled_at', 'temp_f_display')
    read_only = ('id', 'sampled_at', 'temp_f_display')

admin.site.register(SensorSample, SensorSampleAdmin)
