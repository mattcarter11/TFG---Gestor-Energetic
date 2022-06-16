from abc import ABC, abstractmethod

class DBBase(ABC):

    @abstractmethod
    def create_database(self, database:str):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def create_table(self, table:str):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def insert(self, table, dic:dict):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def query(self, query:str) -> list:
        raise NotImplementedError("Base Class")