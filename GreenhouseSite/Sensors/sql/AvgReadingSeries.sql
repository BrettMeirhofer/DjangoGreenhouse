SELECT reading_datetime, round(AVG(value),2)
FROM Sensors_reading
WHERE sensor_id=%s
GROUP BY DATE_FORMAT(reading_datetime, %s)
ORDER BY reading_datetime desc
LIMIT 10