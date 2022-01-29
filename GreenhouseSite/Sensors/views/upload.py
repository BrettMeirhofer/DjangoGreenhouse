from django.http import HttpResponse
import json
import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .. import models
from rest_framework.authentication import TokenAuthentication
from . import view_helpers as helper


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_temp_reading(request):
    if request.method == "POST":
        temp_data = json.loads(request.body.decode("utf-8"))
        current_time = helper.get_remote_time(temp_data)
        sensors = [8, 9, 10, 11]
        helper.bulk_readings(temp_data, sensors, current_time)
    return HttpResponse("Success")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_soil_reading(request):
    if request.method == "POST":
        temp_data = json.loads(request.body.decode("utf-8"))
        current_time = helper.get_remote_time(temp_data)
        sensors = [5, 6, 7]
        helper.bulk_readings(temp_data, sensors, current_time)
    return HttpResponse("Success")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_water_reading(request):
    if request.method == "POST":
        water_data = json.loads(request.body.decode("utf-8"))
        current_time = helper.get_remote_time(water_data)
        water_reading = models.Reading(sensor_id=4, value=round(water_data["water_level"]*100, 2),
                                       reading_datetime=current_time)
        water_reading.save()
    return HttpResponse("Success")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_device_status(request):
    if request.method == "POST":
        device_data = json.loads(request.body.decode("utf-8"))
        current_time = helper.get_remote_time(device_data)
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
        image_model = models.DatedImage(image=file_uploaded, date=datetime.datetime.now().date())
        image_model.save()

    return HttpResponse("Success")
