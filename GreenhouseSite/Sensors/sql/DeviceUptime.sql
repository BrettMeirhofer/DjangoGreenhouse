SELECT status_datetime, (1000 * sum(status)) / count(*)
FROM Sensors_devicestatus
WHERE device_id=%s
GROUP BY DATE_FORMAT(status_datetime, %s)
ORDER BY status_datetime desc
LIMIT 10