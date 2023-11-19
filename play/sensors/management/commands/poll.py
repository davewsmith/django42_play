from django.core.management.base import BaseCommand, CommandError
from sensors.models import Sensor, SensorSample


class Command(BaseCommand):
    help = "Polls sensors and record samples"

    def handle(self, *args, **options):
        sensors = Sensor.objects.all()

        # TODO, maybe: De-dupe sensors so as to sample each only once
        for sensor in sensors:
            Sensor.sample(sensor)
            self.stdout.write(
                self.style.SUCCESS(f'Polled sensor {sensor.sensor_id}')
            )
