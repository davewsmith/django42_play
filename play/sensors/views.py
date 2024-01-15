import logging

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Sensor, SensorSample


logger = logging.getLogger(__name__)


class SensorIdForm(forms.Form):
    sensor_id = forms.IntegerField()


def index(request):
    if not request.user.is_authenticated:
        # Punt login to Admin
        return HttpResponseRedirect('/admin')

    if request.method == 'POST':
        form = SensorIdForm(request.POST)
        if form.is_valid():
            logger.info("form is valid")
            # TODO additional checks
            sensor_id = form.cleaned_data['sensor_id']
            sensor = Sensor(user=request.user, sensor_id=sensor_id)
            sensor.save()
            return HttpResponseRedirect("/")  # TODO
        else:
            logger.info("form isn't valid")
            return HttpResponseRedirect("/")  # TODO
    else:
        form = SensorIdForm()
    samples = SensorSample.objects.order_by('-id').all()
    context = {
        'samples': samples,
        'form': form,
    }
    return render(request, 'sensors/index.html', context)
