from . import view_helpers as helper
from .. import models
from django.http import HttpResponse
import json
import datetime


# Returns a json of avg temp per hour for last 10 hours
def get_temp_series(request):
    response_data = helper.sensor_series([8], helper.fah_to_cel, file="AvgReadingSeries.sql")
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Returns a json of avg humidity per hour for last 10 hours
def get_humd_series(request):
    response_data = helper.sensor_series([9], file="AvgReadingSeries.sql")
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Returns a json of avg water level per hour for last 10 hours
def get_water_series(request):
    response_data = helper.sensor_series([4], int, file="AvgReadingSeries.sql")
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_heater_series(request):
    response_data = helper.sensor_series([1], lambda x: x/10, file="DeviceUptime.sql")
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Returns a json of most recent sensor data / device status
def request_sensor_data(request):
    temp = models.Reading.objects.filter(sensor__sensor_name="Greenhouse Temperature").latest("reading_datetime").value
    humd = models.Reading.objects.filter(sensor__sensor_name="Greenhouse Humidity").latest("reading_datetime").value
    water = models.Reading.objects.filter(sensor__sensor_name="Reservoir Sonar").latest("reading_datetime").value
    heater = models.DeviceStatus.objects.filter(device__device_name="Heater").latest("status_datetime").status
    json_output = {"readings": [temp, humd, int(water)], "heater": heater}
    soil_sensors = [5, 6, 7]

    for sensor in soil_sensors:
        moisture = models.Reading.objects.filter(sensor_id=sensor).latest("reading_datetime").value
        status = helper.find_soil_status(moisture)
        json_output["readings"].append(status)

    return HttpResponse(json.dumps(json_output), content_type="application/json")
