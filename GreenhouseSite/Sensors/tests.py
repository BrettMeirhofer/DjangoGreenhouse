from django.test import TestCase
from Sensors.views import view_helpers as helpers
from Sensors import models
from django.utils import timezone
import datetime
import pytz


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
        sql_output = helpers.connection_query("DeviceUptime.sql", [1, "h"])
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

    def test_datetime_now(self):
        self.assertEqual(timezone.now().replace(tzinfo=None), datetime.datetime.utcnow())


# Tests the get_x_delta group of functions in view_helpers
class HelperDeltaTestCase(TestCase):
    base_date = datetime.datetime.strptime("20220126", "%Y%m%d")

    # Checks that the day delta between two identical dates is 0
    def test_delta_days_same(self):
        day_delta = helpers.get_delta_days(self.base_date, self.base_date)
        self.assertEqual(day_delta, 0)

    # Checks that the day delta between two dates that are 2 days apart is 2
    def test_delta_days_two(self):
        current_date = datetime.datetime.strptime("20220128", "%Y%m%d")
        day_delta = helpers.get_delta_days(self.base_date, current_date)
        self.assertEqual(day_delta, 2)

    def test_delta_months_same(self):
        day_delta = helpers.get_delta_months(self.base_date, self.base_date)
        self.assertEqual(day_delta, 0)

    def test_delta_months_two(self):
        current_date = datetime.datetime.strptime("20220326", "%Y%m%d")
        day_delta = helpers.get_delta_months(self.base_date, current_date)
        self.assertEqual(day_delta, 2)

