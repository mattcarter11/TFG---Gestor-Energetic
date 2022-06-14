# Simulació

## Dades d'entrada

 - Potència produïda                (format .csv -> timestamp, powerG)
 - Potència produïda i Consumida    (format .csv -> timestamp, powerG, powerC)

## Dades de sortida

### Potència per mostra
 
| Variable | Descripció                    |
| :------: | :-----------------------------|
| powerG   | Generada                      |
| powerC   | Consumida Total               |
| powerLB  | Consumida per la càrrega base |
| powerL1  | Consumida per la càrrega 1    |

### Energia per mostra

| Variable | Descripció                    |
| :------: | :-----------------------------|
| energyP  | Produïda                      |
| energyA  | Disponible                    |

### Energia per hora / total / diaria

| Variable | Descripció                    |
| :------: | :-----------------------------|
| energyP  | Produïda                      |
| energyA  | Disponible                    |
| energyG  | Agafada de la Xarxa           |
| energyCM | Consum Total Màxim            |
| energyC  | Consumida Total               |
| energyLB | Consumida per la càrrega base |
| energyL1 | Consumida per la càrrega 1    |
| energyS  | Sobreixida / Excedent         |
| energyL  | Perduda / Podria consumir-se  |

### Info total de cada carrega

 - Commutacions totals (per simulació i diariament)
 - Temps Funcionant (en mostres, hores i diariament)


# TO DO

## trobar costos

- venut -> preu fix (ingrés pk no tens més càrrega i ingrés pk no s'ha engegat càrrega)

## Implementar algoriszme Necessito
- Accés VPN Rasbperry Jordi
- Base de dades al arnau
- Codi per fer el driver i parlar amb les plaques
- Com fer el control de les càrregues

# InfluxDB cli export csv
- influx -host 10.10.10.100 -port 18086 -database 'gestor-energetic-SVC' -execute 'SELECT * FROM hysteresis' -format csv > test.csv



# Canvis a d'algorithme
- 14/06/2022 a les 19:00