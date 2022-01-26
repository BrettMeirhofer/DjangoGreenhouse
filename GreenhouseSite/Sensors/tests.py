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

    def test_device_uptime(self):
        date_string = "202201260605"
        current_time = datetime.datetime.strptime(date_string, "%Y%m%d%H%M")
        current_time = pytz.utc.localize(current_time)
        models.Device(id=1, device_name="TestDevice").save()

        objects = []
        for x in [0, 0, 1, 1]:
            status = models.DeviceStatus(device_id=1, status_datetime=current_time, status=bool(x))
            objects.append(status)
        models.DeviceStatus.objects.bulk_create(objects)
        sql_output = helpers.connection_query("DeviceUptime.sql", None)
        expected_output = [(current_time.strftime("%Y%m%d%H"), 500)]
        self.assertEqual(sql_output, expected_output)

    def test_remote_time(self):
        date_string = "202201260530"
        aware = helpers.get_remote_time({"date": date_string})
        self.assertEqual("date_string", aware.strftime("%Y%m%d%H%M"))
