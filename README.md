# What is this

This is my TFG project while suding TIC at UPC of Manresa. I really recomend reading the document *Memòria del TFG* where everithing is explained in detail.

## Project Summary

In Spain, if you have renewable energy porduction, your energy bill goes as follows: At the end of every hour your energy balance is calculated (energyConsumed - energyProduced). 
- If you have consumed more energy that produced, you must pay that difference. Which can get very expensive depending on the hour. 
- If instead you have produced more that consumed, the company has to pay. But the price they pay is around half of the lowest hour price, which is not very good. 

Thanks to this hour slot system you can, for example, consume 1 kWh of energy in the first 10 min and then produce 1kWh during 20 min, thus having a net zero consumption and not paying anything. 

This project aims to create, analize and compare diferent algorithms which manag loads adequately so to achieve: the màximum energy bill price reduction (try to get to 0), maximise the use of the energy produced, and minimize the number of load commutations.

A simulator has been implemented to test and analize the algorithms. With it, the best settings can be found before implementing the system in real life. Once found, the algorithms have been implemented and tested in real life.

# File and folder structure

- *doc*: contains the project paper (Memòria del TFG).
- *sim*: contains the simulator
    - *main.py*: the main program of the simulator
    - *db*: real data .scv files used to test and obtain the paper results
    - *lib*: contains all the created modules used by *main.py*
        - *myQT*: contains custom QT Widgets used for the GUI
        - *sim*: class and function used for simulating and calculating the results.
- *src*: contains scripts implemented in real life.
    - *managin.py*: a script that manages two loads
    - *monitoring.py*: a script that monitors the powers and energies of the instalation
    - *stop_loads.py*: a script that stops the two loads
    - *drivers*: contains the drivers for interacting with the DataBase, the Laoad and the PowerMeter
    - *daemons*: contains the two systemd daemons for running the load manager and the sistem monitoring.

# Simulating

1. Inside *sim* run: `pip install -r requirements.txt`
2. Run the *main.py* script
3. Enjoy the simulator

# Installing the manager and monitoring

1. Copy the *src* folder tot your server (e.g. Raspberry)
2. Inside *src* run: `pip install -r requirements.txt`
3. Move the daemons folder contents to */etc/systemd/system*
4. Configure them adequatly (user, foder where the script is located, ...)
5. Create the database using the corresponding method
6. Create your won drivers if needed 
7. Configure each script by changing the *settings* section
8. Start the daemons

# Daemon
There are two daemons, ge-managing & ge-monitoring, one for each script, managing.py & monitoring.py (ge stands for 'Gestor Energèrtic`).
- Install: copiar a la carpeta */etc/systemd/system*
- Edit: `sudo systemctl --force --full edit <nom>` 
- Start/Stop/Restart: `sudo systemctl [start|stop|restart] <nom>`
    - If the settings of the script are changes, you need to restart the daemon

# InfluxDB CLI

  - Acces: `influx -host <ip> [-port <port>]`
  - Accedir the database: `use <database>`
    - If we have `InfluxDB('10.10.10.100', 18086, 'gestor-energetic-SVC')` in the script, then de do `use gestor-energetic-SVC`
  - See a the table data: `select * from <table>`
  - Clear table: `delete from <table>`

