from os import path
from django.db import connection
import pytz
from django.utils import timezone
from .. import models
import datetime


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


def bulk_readings(temp_data, sensors, types, current_time):
    reading_objects = []
    for index, reading in enumerate(temp_data["readings"]):
        reading_object = models.Reading(value=reading, sensor_id=sensors[index], reading_type_id=types[index],
                                        reading_datetime=current_time)
        reading_objects.append(reading_object)
    models.Reading.objects.bulk_create(reading_objects)


def get_remote_time(temp_data):
    current_time = datetime.datetime.strptime(temp_data["date"], "%Y%m%d%H%M")
    current_time = timezone.make_aware(current_time, timezone=pytz.timezone("America/Chicago"))
    return current_time
