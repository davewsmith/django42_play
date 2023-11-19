from django.core.management.base import BaseCommand, CommandError
from sensors.models import Sensor, SensorSample


class Command(BaseCommand):
    help = "Polls sensors and record samples"

    def handle(self, *args, **options):
        sensors = Sensor.objects.all()

        for sensor in sensors:
            sample = SensorSample(sensor=sensor, data="fake")
            sample.save()
            self.stdout.write(
                self.style.SUCCESS(f'Fake polled sensor_id {sensor.sensor_id}')
            )
