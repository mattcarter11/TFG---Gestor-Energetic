from abc import ABC, abstractmethod

class DataBase(ABC):

    @abstractmethod
    def create_database(self, database:str): pass

    @abstractmethod
    def create_table(self, table:str): pass

    @abstractmethod
    def insert(self, table, dic:dict): pass