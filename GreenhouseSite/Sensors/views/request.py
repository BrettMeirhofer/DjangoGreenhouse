from . import view_helpers as helper
from .. import models
from django.http import HttpResponse
import json
import datetime
from django.core.serializers.json import DjangoJSONEncoder


# Returns a json of avg temp per hour for last 10 hours
def get_temp_series(request):
    response_data = helper.sensor_series([8], helper.fah_to_cel, increment=request.GET.get('increment', 'h'))
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Returns a json of avg humidity per hour for last 10 hours
def get_humd_series(request):
    response_data = helper.sensor_series([9], increment=request.GET.get('increment', 'h'))
    return HttpResponse(json.dumps(response_data), content_type="application/json")

"""
# Returns a json of avg water level per hour for last 10 hours
def get_water_series(request):
    response_data = helper.sensor_series([1], int, file="AvgTankLevel.sql")
    return HttpResponse(json.dumps(response_data), content_type="application/json")
"""


def get_heater_series(request):
    response_data = helper.sensor_series([1], lambda x: x/10, file="DeviceUptime.sql", increment=request.GET.get('increment', 'h'))
    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")


def get_water_series(request):
    response_data = helper.sensor_series([1], int, file="AvgTankLevel.sql", increment=request.GET.get('increment', 'h'))
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Returns a json of most recent sensor data / device status
def request_sensor_data(request):
    temp = models.Reading.objects.filter(sensor__sensor_name="Greenhouse Temperature").latest("reading_datetime").value
    humd = models.Reading.objects.filter(sensor__sensor_name="Greenhouse Humidity").latest("reading_datetime").value
    temp_out = models.Reading.objects.filter(sensor__sensor_name="Outdoor Temp").latest("reading_datetime").value
    humd_out = models.Reading.objects.filter(sensor__sensor_name="Outdoor Humd").latest("reading_datetime").value
    max_level, current, percent = models.Tank.objects.get(id=1).get_status_dict()
    heater = models.DeviceStatus.objects.filter(device__device_name="Heater").latest("status_datetime").status
    json_output = {"readings": [temp, humd, temp_out, humd_out, percent], "heater": heater}

    return HttpResponse(json.dumps(json_output), content_type="application/json")


