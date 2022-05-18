from .DataBase import DataBase
from influxdb import InfluxDBClient
from datetime import datetime

class InfluxDB(DataBase):

    def __init__(self, host:str, port:int, database:str):
        self.__client = InfluxDBClient(host, port, database=database)

    def create_database(self, database:str):
        self.__client.create_database(database)

    def switch_database(self, database:str): 
        self.__client.switch_database(database)

    def create_table(self, table:str): 
        pass

    def insert(self, table:str, dic:dict):
        json = [
            {
                "measurement": table,
                "time": datetime.utcnow(),
                "fields": dic
            }
        ]
        self.client.write_points(json)