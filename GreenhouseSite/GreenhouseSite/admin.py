from Sensors.views import upload
from django.urls import path
from django.contrib import admin


class GreenhouseAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('Temp/', upload.upload_temp_reading, name="Temp"),
            path('Water/', upload.upload_water_reading, name="Water"),
            path('upload_image/', upload.upload_image, name="upload_image"),
            path('Soil/', upload.upload_soil_reading, name="Soil"),
            path('Device/', upload.upload_device_status, name="Device"),
            path('upload_readings/', upload.upload_readings, name="upload_readings"),
        ]
        return my_urls + urls
