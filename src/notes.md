# InfluxDB cli export csv
- influx -host 10.10.10.100 -port 18086 -database 'gestor-energetic-SVC' -execute 'SELECT * FROM hysteresis' -format csv > test.csv

# Canvis a d'algorithme
- 14/06/2022 a les 19:00
- 15/06/2022 a les 16:00
- 16/06/2022 a les 15:00 -> canvi a predictiu = fail
- 16/06/2022 a les 18:00 -> fixing
- 18/06/2022 all day     -> fixing time to consume (not done, data results)
- 21/06/2022 a les 16:23 -> testing ttc
- 22/06/2022 a les 15:49 -> restart per testing ttc
- 24/06/2022 a les 14:42 -> 150 mon to 70
- 28/06/2022 a les 22:44 -> switch to average_power