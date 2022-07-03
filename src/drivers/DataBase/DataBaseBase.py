from abc import ABC, abstractmethod

class DBBase(ABC):

    @abstractmethod
    def create_database(self, database:str):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def switch_database(self, database:str):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def create_table(self, table:str):
        raise NotImplementedError("Base Class")

    @abstractmethod
    def insert(self, table:str, dic:dict):
        ''' 
        Insert the dict data into the indicated table of the current database.
        Each dict key corresponds to a column of the table 
        '''
        raise NotImplementedError("Base Class")

    @abstractmethod
    def query(self, query:str) -> list:
        '''Run the query on the current database.'''
        raise NotImplementedError("Base Class")