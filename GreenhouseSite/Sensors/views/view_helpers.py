from os import path
from django.db import connection
import pytz
from django.utils import timezone
from .. import models
import datetime
from django.http import HttpResponse
import json


# Copies a sql file into memory then sends it to the database. Database results are returned
def connection_query(filename, parameters):
    sql_path = path.join(path.dirname(path.dirname(__file__)), "sql", filename)
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


def get_delta_hours(target_datetime):
    tz = pytz.timezone("Africa/Abidjan")
    hours = timezone.now() - timezone.make_aware(target_datetime, tz)
    hours = round(hours.seconds/3600, 0)
    return hours


def bulk_readings(temp_data, sensors, types, current_time):
    reading_objects = []
    for index, reading in enumerate(temp_data["readings"]):
        reading_object = models.Reading(value=reading, sensor_id=sensors[index], reading_type_id=types[index],
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
def sensor_series(parameters, y_adjust=None, file="AvgSensorSeries.sql"):
    sql_output = connection_query(file, parameters)

    response_data = {"label": [], "y": []}
    for index, row in enumerate(sql_output):
        label = get_delta_hours(row[0])
        response_data["label"].append(label)
        if y_adjust is not None:
            temp_f = y_adjust(row[1])
        else:
            temp_f = row[1]
        response_data["y"].append(temp_f)

    response_data["y"].reverse()
    response_data["label"].reverse()
    return response_data

