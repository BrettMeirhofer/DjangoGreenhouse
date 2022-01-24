from . import view_helpers as helper
from .. import models
from django.http import HttpResponse
import json


# Returns a json of avg temp per hour for last 10 hours
def get_temp_series(request):
    return sensor_series([1, 2], fah_to_cel, file="AvgReadingSeries.sql")


# Returns a json of avg humidity per hour for last 10 hours
def get_humd_series(request):
    return sensor_series([2, 2], file="AvgReadingSeries.sql")


# Returns a json of avg water level per hour for last 10 hours
def get_water_series(request):
    return sensor_series([3])


# Converts fahrenheit to celsius
def fah_to_cel(row_value):
    output = round((row_value * (9 / 5)) + 32, 2)
    return output


# Builds a json designed for consumption by chart.js graphs from an sql query
def sensor_series(parameters, y_adjust=None, file="AvgSensorSeries.sql"):
    sql_output = helper.connection_query(file, parameters)

    response_data = {"label": [], "y": []}
    for index, row in enumerate(sql_output):
        label = helper.get_delta_seconds(row[0])
        response_data["label"].append(label)
        if y_adjust is not None:
            temp_f = y_adjust(row[1])
        else:
            temp_f = row[1]
        response_data["y"].append(temp_f)

    response_data["y"].reverse()
    response_data["label"].reverse()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Returns a json of avg heater uptime per hour for last 10 hours
def get_heater_series(request):
    sql_output = helper.connection_query("DeviceUptime.sql", None)

    response_data = {"label": [], "y": []}
    for index, row in enumerate(sql_output):
        label = helper.get_delta_seconds(row[0])
        response_data["label"].append(label)
        y = min(int((row[1] / min((label/180), 20)) * 100), 100)
        response_data["y"].append(y)

    response_data["y"].reverse()
    response_data["label"].reverse()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Returns a json of most recent sensor data / device status
def request_sensor_data(request):
    temp = models.Reading.objects.filter(sensor_id=2).filter(reading_type_id=1).latest("reading_datetime").value
    humd = models.Reading.objects.filter(sensor_id=2).filter(reading_type_id=2).latest("reading_datetime").value
    water = models.Reading.objects.filter(reading_type_id=3).latest("reading_datetime").value
    heater = models.DeviceStatus.objects.filter(device_id=1).latest("status_datetime").status
    json_output = {"readings": [temp, humd, water], "heater": heater}
    soil_sensors = [5, 6, 7]
    for sensor in soil_sensors:
        moisture = models.Reading.objects.filter(sensor_id=sensor).latest("reading_datetime").value
        json_output["readings"].append(moisture)

    return HttpResponse(json.dumps(json_output), content_type="application/json")