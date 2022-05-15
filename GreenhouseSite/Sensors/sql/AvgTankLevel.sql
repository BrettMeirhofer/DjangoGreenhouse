SELECT reading_datetime, round(AVG(value),2)
FROM Sensors_reading
WHERE sensor_id=%s
GROUP BY strftime(%s, reading_datetime)
ORDER BY reading_datetime desc
LIMIT 10





