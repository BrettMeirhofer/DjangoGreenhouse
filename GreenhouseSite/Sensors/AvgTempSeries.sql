SELECT reading_datetime, round(AVG(value),2)
FROM Sensors_Reading
WHERE reading_type_id=%s
GROUP BY reading_datetime
ORDER BY reading_datetime desc
LIMIT 10