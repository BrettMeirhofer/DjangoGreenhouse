from django.test import TestCase
from Sensors.views import view_helpers as helpers
from Sensors import models
from django.utils import timezone
import datetime
import pytz


def test_delta_days(target_string, current_string):
    target_date = datetime.datetime.strptime(target_string, "%Y%m%d")
    current_date = datetime.datetime.strptime(current_string, "%Y%m%d")
    tz = pytz.timezone("Africa/Abidjan")
    current_date = timezone.make_aware(current_date, tz)
    day_delta = helpers.get_delta_days(target_date, current_date)
    return day_delta


class ViewHelpersTestCase(TestCase):
    # Checks that sql directory can be found, the query executed on the db, and the results returned
    def test_connection_query(self):
        names = ["test1", "test2"]
        objects = []
        for name in names:
            objects.append(models.SensorType(type_name=name))
        models.SensorType.objects.bulk_create(objects)
        sql_output = helpers.connection_query("GetSensorTypes.sql", None)
        expected_output = [(1, "test1"), (2, "test2")]
        self.assertEqual(sql_output, expected_output)

    # Checks that device uptime ca
    def test_device_uptime(self):
        date_string = "202201260605"
        current_time = datetime.datetime.strptime(date_string, "%Y%m%d%H%M")
        models.Device(id=1, device_name="TestDevice").save()
        current_time = pytz.utc.localize(current_time)
        objects = []
        for x in [0, 0, 1, 1]:
            status = models.DeviceStatus(device_id=1, status_datetime=current_time, status=bool(x))
            objects.append(status)
        models.DeviceStatus.objects.bulk_create(objects)
        sql_output = helpers.connection_query("DeviceUptime.sql", [1])
        expected_output = [(current_time.replace(tzinfo=None), 500)]
        self.assertEqual(sql_output, expected_output)

    def test_remote_time(self):
        date_string = "202201260530"
        aware = helpers.get_remote_time({"date": date_string})
        self.assertEqual(date_string, aware.strftime("%Y%m%d%H%M"))

    def test_find_soil_status_v_wet(self):
        self.assertEqual(helpers.find_soil_status(0), "Very Wet")

    def test_find_soil_status_v_dry(self):
        self.assertEqual(helpers.find_soil_status(55000), "Very Dry")


# Tests the get_x_delta group of functions in view_helpers
class HelperDeltaTestCase(TestCase):
    # Checks that the day delta between two identical dates is 0
    def test_delta_days_same(self):
        date_string = "20220126"
        self.assertEqual(test_delta_days(date_string, date_string), 0)

    # Checks that the day delta between two dates that are 2 days apart is 2
    def test_delta_days_two(self):
        self.assertEqual(test_delta_days("20220126", "20220128"), 2)
