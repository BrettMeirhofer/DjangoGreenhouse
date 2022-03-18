from django.http import HttpResponse
import json
import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .. import models
from rest_framework.authentication import TokenAuthentication
from . import view_helpers as helper


# Endpoint for uploading readings for temp/humd sensors
# Now used for triggering an outdoor conditions update
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_temp_reading(request):
    helper.get_outdoor_weather()
    return HttpResponse("Success")


# Endpoint for uploading readings for soil moisture sensors
# Will be phased out
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


# Endpoint for uploading readings for water level sensor
# Will be phased out
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_water_reading(request):
    if request.method == "POST":
        water_data = json.loads(request.body.decode("utf-8"))
        current_time = helper.get_remote_time(water_data)
        water_reading = models.Reading(sensor_id=4, value=round(water_data["water_level"] * 100, 2),
                                       reading_datetime=current_time)
        water_reading.save()
    return HttpResponse("Success")


# Endpoint for uploading generic reading/sensor_id pairs
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_readings(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        current_time = helper.get_remote_time(json_data)
        reading_objects = []
        for reading_data in json_data["readings"]:
            reading_objects.append(models.Reading(sensor_id=reading_data["s"], value=reading_data["r"],
                                                  reading_datetime=current_time))

        models.Reading.objects.bulk_create(reading_objects)
    return HttpResponse("Success")


# Endpoint for uploading generic device status updates
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


# Endpoint for uploading dated images
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_image(request):
    if request.method == "POST":
        file_uploaded = request.FILES.get('file_uploaded')
        cam_id = request.GET.get('id', '')
        image_model = models.DatedImage(image=file_uploaded, date=datetime.datetime.now().date(), camera_id=int(cam_id))
        image_model.make_thumbnail()
        image_model.save()
    return HttpResponse("Success")
