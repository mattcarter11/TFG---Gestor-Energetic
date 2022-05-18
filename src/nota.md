El projecte és troba a /home/pi2/TFG

  - *managing.py* és el gestor
  - *monitoring.py* és el monitoratge
  - Els paràmetres de cada script es configuren al inici d'aquest
  - */drivers* conté els drivers específic

El daemons es diuen ge-managing i ge-monitoring respectivament

  - Instal·lar: copiar a la carpeta */etc/systemd/system*
  - Editar: `sudo systemctl --force --full edit <nom>` 
  - Iniciar/Parar/Reiniciar: `sudo systemctl [start|stop|restart] <nom>`
    - Si es cambia la configuració del script, s'ha de reiniciar el daemon

InfluxDB per CLI

  - Accedir-hi: `influx -host 10.10.10.100 -port 18086`
  - Accedir a la  base de dades del TFG: `use gestor-energetic`
  - Veure dades de la taula: `select * from hysteresis`
  - Eliminar les dades: `delete from hysteresis`