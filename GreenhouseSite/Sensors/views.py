from django.http import HttpResponse
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
from django.core import exceptions


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
        bulk_readings(temp_data, sensors, types, current_time)
        device_update = models.DeviceStatus(device_id=1, status=temp_data["heater"], status_datetime=current_time)
        device_update.save()
    return HttpResponse("Success")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_soil_reading(request):
    if request.method == "POST":
        temp_data = json.loads(request.body.decode("utf-8"))
        current_time = get_remote_time(temp_data)
        sensors = [5, 6, 7]
        types = [4, 4, 4]
        bulk_readings(temp_data, sensors, types, current_time)
    return HttpResponse("Success")


def bulk_readings(temp_data, sensors, types, current_time):
    reading_objects = []
    for index, reading in enumerate(temp_data["readings"]):
        reading_object = models.Reading(value=reading, sensor_id=sensors[index], reading_type_id=types[index],
                                        reading_datetime=current_time)
        reading_objects.append(reading_object)
    models.Reading.objects.bulk_create(reading_objects)


def get_remote_time(temp_data):
    current_time = datetime.datetime.strptime(temp_data["date"], "%Y%m%d%H%M")
    current_time = make_aware(current_time, timezone=pytz.timezone("America/Chicago"))
    return current_time


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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_device_status(request):
    if request.method == "POST":
        device_data = json.loads(request.body.decode("utf-8"))
        current_time = datetime.datetime.strptime(device_data["date"], "%Y%m%d%H%M")
        current_time = make_aware(current_time, timezone=pytz.timezone("America/Chicago"))
        device_status = models.DeviceStatus(device_id=device_data["device"], status=device_data["status"],
                                            status_datetime=current_time)
        device_status.save()
    return HttpResponse("Success")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_image(request):
    if request.method == "POST":
        file_uploaded = request.FILES.get('file_uploaded')
        print(request.FILES)
        content_type = file_uploaded.content_type
        image_model = models.DatedImage(image=file_uploaded, date=datetime.datetime.now().date())
        image_model.save()
        print(content_type)

    return HttpResponse("Success")


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


# Displays a page listing realtime information about the greenhouse
def greenhouse_status(request):
    try:
        latest_image = models.DatedImage.objects.latest("date").image.url
    except exceptions.ObjectDoesNotExist:
        latest_image = ""

    return render(request, "admin/dashboard.html", {'img_url': latest_image})


def get_temp_series(request):
    return sensor_series([1, 2], fah_to_cel, file="AvgReadingSeries.sql")


def get_humd_series(request):
    return sensor_series([2, 2], file="AvgReadingSeries.sql")


def get_water_series(request):
    return sensor_series([3])


def fah_to_cel(row_value):
    output = round((row_value * (9 / 5)) + 32, 2)
    return output


def sensor_series(parameters, y_adjust=None, file="AvgSensorSeries.sql"):
    sql_output = connection_query(file, parameters)

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
    sql_path = path.join(path.dirname(__file__), "sql", filename)
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


def gallery_view(request):
    urls = models.DatedImage.objects.order_by("date").values_list("image", flat=True).url
    print(urls)
    return render(request, "admin/gallery.html", {'url_list': urls})
