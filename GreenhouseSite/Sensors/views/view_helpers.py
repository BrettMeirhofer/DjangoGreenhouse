from os import path
from django.db import connection
import pytz
from .. import models
import datetime
from django.conf import settings as conf_settings
import requests


# Copies a sql file into memory then sends it to the database. Database results are returned
def connection_query(filename, parameters):
    sql_path = path.join(path.dirname(path.dirname(__file__)), "sql", filename)
    sql_text = open(sql_path).read()
    with connection.cursor() as cursor:
        cursor.execute(sql_text, parameters)
        sql_output = cursor.fetchall()
    return sql_output


def get_delta_seconds(target_datetime, current_time=datetime.datetime.utcnow()):
    return round((current_time - target_datetime).seconds, 0)


def get_delta_hours(target_datetime, current_time=datetime.datetime.utcnow()):
    target_datetime = target_datetime.replace(minute=0, second=0)
    return round((current_time - target_datetime).seconds/3600, 0)


def get_delta_days(target_datetime, current_time=datetime.datetime.utcnow()):
    target_datetime = target_datetime.replace(hour=0, minute=0, second=0)
    return round((current_time - target_datetime).days, 0)


def get_delta_months(target_datetime, current_time=datetime.datetime.utcnow()):
    return round((current_time.month - target_datetime.month), 0)


def bulk_readings(temp_data, sensors, current_time):
    reading_objects = []
    for index, reading in enumerate(temp_data["readings"]):
        reading_object = models.Reading(value=reading, sensor_id=sensors[index],
                                        reading_datetime=current_time)
        reading_objects.append(reading_object)
    models.Reading.objects.bulk_create(reading_objects)


def get_remote_time(temp_data):
    current_time = datetime.datetime.strptime(temp_data["date"], "%Y%m%d%H%M")
    current_time = pytz.utc.localize(current_time)
    return current_time


# Converts fahrenheit to celsius
def fah_to_cel(row_value):
    output = round((row_value * (9 / 5)) + 32, 2)
    return output


# Builds a json designed for consumption by chart.js graphs from an sql query
def sensor_series(parameters, y_adjust=None, file="AvgReadingSeries.sql", increment="h"):
    increment_list = get_increment(increment)
    parameters.append(increment_list[0])
    sql_output = connection_query(file, parameters)

    response_data = {"label": [], "y": []}
    for index, row in enumerate(sql_output):
        label = increment_list[1](row[0])
        response_data["label"].append(label)
        if y_adjust is not None:
            temp_f = y_adjust(row[1])
        else:
            temp_f = row[1]
        response_data["y"].append(temp_f)


    response_data["y"].reverse()
    response_data["label"].reverse()
    return response_data


def find_soil_status(value):
    soil_status = [[0, "Very Wet"], [40000, "Wet"], [50000, "Dry"], [55000, "Very Dry"]]
    soil_status.reverse()
    for status in soil_status:
        if value >= status[0]:
            return status[1]
    return "Error"


def get_increment(key):
    increment_dict = {"h": ["'%Y%m%d%H'", get_delta_hours], "d": ["'%Y%m%d'", get_delta_days], "m": ["'%Y%m'", get_delta_days]}
    return increment_dict[key]


def get_outdoor_weather():
    target_url = "https://api.weatherapi.com/v1/current.json"
    r = requests.get(target_url, params={"key": conf_settings.OUTDOOR_KEY, "q": conf_settings.OUTDOOR_ZIP})
    current_time = datetime.datetime.utcnow()
    current_time = pytz.utc.localize(current_time)
    temp = r.json()["current"]["temp_c"]
    humd = r.json()["current"]["humidity"]
    temp_sensor = models.Sensor.objects.get(sensor_name="Outdoor Temp").id
    humd_sensor = models.Sensor.objects.get(sensor_name="Outdoor Humd").id
    read_1 = models.Reading(sensor_id=temp_sensor, reading_datetime=current_time, value=temp)
    read_2 = models.Reading(sensor_id=humd_sensor, reading_datetime=current_time, value=humd)
    models.Reading.objects.bulk_create([read_1, read_2])
