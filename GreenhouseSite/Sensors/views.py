from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from os import path
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from . import models
from rest_framework.authentication import TokenAuthentication
from django.db import connection
from django.shortcuts import render
from django.utils.timezone import make_aware
import pytz
from django.utils import timezone


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_temp_reading(request):
    if request.method == "POST":
        temp_data = json.loads(request.body.decode("utf-8"))
        current_time = datetime.datetime.strptime(temp_data["date"], "%Y%m%d%H%M")
        current_time = make_aware(current_time, timezone=pytz.timezone("America/Chicago"))
        sensors = [2, 2, 3, 3]
        types = [1, 2, 1, 2]
        reading_objects = []

        for index, reading in enumerate(temp_data["readings"]):
            reading_object = models.Reading(value=reading, sensor_id=sensors[index], reading_type_id=types[index],
                                            reading_datetime=current_time)
            reading_objects.append(reading_object)

        models.Reading.objects.bulk_create(reading_objects)
        device_update = models.DeviceStatus(device_id=1, status=temp_data["heater"], status_datetime=current_time)
        device_update.save()
    return HttpResponse("Success")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_water_reading(request):
    if request.method == "POST":
        water_data = json.loads(request.body.decode("utf-8"))
        current_time = datetime.datetime.strptime(water_data["date"], "%Y%m%d%H%M")
        current_time = make_aware(current_time, timezone=pytz.timezone("America/Chicago"))
        water_reading = models.Reading(sensor_id=4, value=round(water_data["water_level"]*100, 2), reading_type_id=3,
                                       reading_datetime=current_time)
        water_reading.save()
    return HttpResponse("Success")


def request_sensor_data(request):
    sql_path = path.join(path.dirname(__file__), "AvgSensorData.sql")
    sql_text = open(sql_path).read()
    with connection.cursor() as cursor:
        cursor.execute(sql_text)
        sql_output = cursor.fetchall()

    json_output = {"readings": []}
    for item in sql_output:
        json_output["readings"].append(item[0])

    json_output["heater"] = models.DeviceStatus.objects.filter(device_id=1).order_by("-status_datetime")[0].status
    print(json_output["heater"])
    return HttpResponse(json.dumps(json_output), content_type="application/json")


# Displays a page listing realtime information about the greenhouse
def greenhouse_status(request):
    return render(request, "admin/sensor_status.html")


def get_temp_series(request):
    return sensor_series(1, fah_to_cel)


def get_humd_series(request):
    return sensor_series(2)


def get_water_series(request):
    return sensor_series(3)


def fah_to_cel(row_value):
    output = round((row_value * (9 / 5)) + 32, 2)
    return output


def sensor_series(reading_type, y_adjust=None):
    sql_output = connection_query("AvgTempSeries.sql", [reading_type])

    response_data = {"label": [], "y": []}
    for index, row in enumerate(sql_output):
        label = get_delta_seconds(row[0])
        response_data["label"].append(label)
        if y_adjust is not None:
            temp_f = y_adjust(row[1])
        else:
            temp_f = row[1]
        response_data["y"].append(temp_f)

    response_data["y"].reverse()
    response_data["label"].reverse()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_heater_series(request):
    sql_output = connection_query("DeviceUptime.sql", None)

    response_data = {"label": [], "y": []}
    for index, row in enumerate(sql_output):
        label = get_delta_seconds(row[0])
        response_data["label"].append(label)
        y = min(int((row[1] / min((label/180), 20)) * 100), 100)
        response_data["y"].append(y)

    response_data["y"].reverse()
    response_data["label"].reverse()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Copies a sql file into memory then sends it to the database. Database results are returned
def connection_query(filename, parameters):
    sql_path = path.join(path.dirname(__file__), filename)
    sql_text = open(sql_path).read()
    with connection.cursor() as cursor:
        cursor.execute(sql_text, parameters)
        sql_output = cursor.fetchall()
    return sql_output


# Given a UTC-0 date return how many seconds ago it occurred
def get_delta_seconds(target_datetime):
    tz = pytz.timezone("Africa/Abidjan")
    seconds = timezone.now() - timezone.make_aware(target_datetime, tz)
    seconds = round(seconds.seconds, 0)
    return seconds
