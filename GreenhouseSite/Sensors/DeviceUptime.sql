SELECT status_datetime, sum(status)
FROM Sensors_DeviceStatus
WHERE device_id=1
GROUP BY strftime('%Y%m%d%H', status_datetime)
ORDER BY status_datetime desc
LIMIT 10