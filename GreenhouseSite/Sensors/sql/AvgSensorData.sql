SELECT ROUND(AVG(value), 2)
FROM
(
SELECT sensor_id, reading_type_id, value, MAX(reading_datetime) AS Latest
FROM Sensors_Reading
GROUP BY sensor_id, reading_type_id
)
GROUP BY reading_type_id




