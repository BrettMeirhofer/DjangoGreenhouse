from django.urls import path, include
from Sensors.views import public
from .views import request

urlpatterns = [
    path('sensor_data', request.request_sensor_data, name='sensor_data'),
    path('temp_series', request.get_temp_series, name='temp_series'),
    path('humd_series', request.get_humd_series, name='humd_series'),
    path('water_series', request.get_water_series, name='water_series'),
    path('heater_series', request.get_heater_series, name='heater_series'),
    path("", public.greenhouse_status, name="dashboard"),
    path("gallery", public.gallery_view, name="gallery"),
    path("progress", public.progress_view, name="progress"),
    path("plants", public.plants_view, name="plants"),
    path("graphs", public.graphs_page, name="graphs")
]