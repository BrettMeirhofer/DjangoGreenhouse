SELECT reading_datetime, round((AVG(value) - sensor_dist) / height, 2)
FROM Sensors_reading
JOIN Sensors_tank ON Sensors_tank.level_sensor_id = Sensors_reading.sensor_id
WHERE Sensors_tank.id = %s
GROUP BY DATE_FORMAT(reading_datetime, %s)
ORDER BY reading_datetime desc
LIMIT 10




