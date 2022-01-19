import requests
import json
import datetime


def send_sensor_data(json_data):
    target_url = "http://192.168.1.21:8000/admin/Water/"
    headers = {"Authorization": "Token 93c5d00d515c440c1e22651b486223f5b7401628"}
    r = requests.post(target_url, data=json.dumps(json_data), headers=headers, allow_redirects=False)


def send_dummy_sensor_data():
    current_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
    data = {"date": current_date_time, "water_level": "50.45"}
    send_sensor_data(data)

send_dummy_sensor_data()