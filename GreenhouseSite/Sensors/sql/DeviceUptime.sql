SELECT status_datetime, (1000 * sum(status)) / count(*)
FROM Sensors_DeviceStatus
WHERE device_id=%s
GROUP BY strftime(%s, status_datetime)
ORDER BY status_datetime desc
LIMIT 10