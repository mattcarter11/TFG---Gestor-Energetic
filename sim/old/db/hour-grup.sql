SELECT max(timestamp) timestamp, value
FROM energy
GROUP BY strftime ('%H',timestamp)
