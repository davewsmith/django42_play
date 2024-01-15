from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Sensor, SensorSample


class SensorIdForm(forms.Form):
    sensor_id = forms.IntegerField()


def index(request):
    if request.method == 'POST':
        form = SensorIdForm(request.POST)
        if form.is_valid():
            # TODO additional checks
            sensor_id = form.cleaned_data['sensor_id']
            sensor = Sensor(user=request.user, sensor_id=sensor_id)
            sensor.save()
            return HttpResponseRedirect("/")  # TODO
        else:
            return HttpResponseRedirect("/")  # TODO
    else:
        form = SensorIdForm()
    samples = SensorSample.objects.order_by('-id').all()
    context = {
        'samples': samples,
        'form': form,
    }
    return render(request, 'sensors/index.html', context)
