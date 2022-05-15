SELECT (reading_datetime - Sensors_tank.sensor_dist) / Sensors_tank.height, round(AVG(value),2)
FROM Sensors_reading
JOIN Sensors_tank ON Sensors_tank.level_sensor_id = reading_datetime.id
WHERE Sensors_tank.id = %s
GROUP BY strftime(%s, reading_datetime)
ORDER BY reading_datetime desc
LIMIT 10




