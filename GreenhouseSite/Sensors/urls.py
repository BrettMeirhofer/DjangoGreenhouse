from django.urls import path

from . import views

urlpatterns = [
    path('sensor_data', views.request_sensor_data, name='sensor_data'),
    path('temp_series', views.get_temp_series, name='temp_series'),
    path('humd_series', views.get_humd_series, name='humd_series'),
    path('water_series', views.get_water_series, name='water_series'),
    path('heater_series', views.get_heater_series, name='heater_series'),
]