from .DataBaseBase import DBBase
from influxdb import InfluxDBClient
from datetime import datetime

class InfluxDB(DBBase):

    def __init__(self, host:str, port:int, database:str):
        self.__client = InfluxDBClient(host, port, database=database)

    def create_database(self, database:str):
        self.__client.create_database(database)

    def switch_database(self, database:str): 
        self.__client.switch_database(database)

    def create_table(self, table:str): 
        pass

    def insert(self, table:str, dic:dict):
        try:
            json = [
                {
                    "measurement": table,
                    "time": datetime.utcnow(),
                    "fields": dic
                }
            ]
            self.__client.write_points(json)
        except:
            pass
        
    def query(self, query:str) -> list:
        results = []
        try:
            for table in self.__client.query(query):
              for record in table:
                results.append(record)
        except:
            pass
        return results