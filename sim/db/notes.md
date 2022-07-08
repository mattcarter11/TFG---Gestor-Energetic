# InfluxDB cli export csv
```
influx -host 10.10.10.100 -port 18086 -database 'gestor-energetic-SVC' -execute 'SELECT * FROM hysteresis' -format csv > test.csv
```


# Dates algorithme

## Histoprial
Si fallava tornava a posar temporalment la histèresis
- 16/06/2022 a les 15:00 -> canvi a predictiu = fail
- 16/06/2022 a les 18:00 -> fixing
- 18/06/2022 all day     -> fixing time to consume (not done, data results)
- 21/06/2022 a les 16:23 -> testing ttc
- 22/06/2022 a les 15:49 -> restart per testing ttc (no predict)
- 24/06/2022 a les 14:42 -> 150 min to 70
- 28/06/2022 a les 22:44 -> switch to average_power (didnt work correctly)
- 04/07/2022 a les 19:44 -> switch to min_on_time (didnt work correctly)
- 04/07/2022 a les 23:00 -> switch to none
- 06/07/2022 a les 15:45 -> switch to average_power (didnt work correctly)
- 06/07/2022 a les 16:15 -> might fixed the problem (didn't work)
- 07/07/2022 a les 15:10 -> might fixed the problem (now wierd power on at nigth)

## histèresis
**Dies OK** 22/04/2022..15/06/2022 

**Config** (en principi tots els dies)
 - th_top1 = 100
 - th_bottom1 = -10 
 - th_top2 = 170
 - th_bottom2 = 100

**Altres** alguns dies són amb Temsp mínim engegat a 600, però no funcionà


## Predictiu
**Dies OK** 06/07/2022 a les 16:15..

**Config**
 - predict = PredictFinalEnergy.project_current_power
 - end_at_energy = 20
 - time_factor = 0.9
 - on_min_energy = 70

