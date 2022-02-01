from django.urls import path

from .views import request

urlpatterns = [
    path('sensor_data', request.request_sensor_data, name='sensor_data'),
    path('temp_series', request.get_temp_series, name='temp_series'),
    path('humd_series', request.get_humd_series, name='humd_series'),
    path('water_series', request.get_water_series, name='water_series'),
    path('heater_series', request.get_heater_series, name='heater_series'),
    path('temp_series_days', request.get_temp_series, name='temp_series_days'),
    path('humd_series_days', request.get_humd_series, name='humd_series_days'),
    path('water_series_days', request.get_water_series, name='water_series_days'),
    path('heater_series_days', request.get_heater_series, name='heater_series_days'),
]