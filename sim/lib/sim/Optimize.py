from re import T
from matplotlib.pyplot import axes
import pandas as pd
from pyparsing import col
from .Results import Results

class Optimize:

    def __init__(self, index_name:str, columns:list[str]):
        self.columns = columns
        self.df = pd.DataFrame(columns=[index_name]+columns)

    def add_results(self, index:int, results:Results):
        l = [index]
        for column in self.columns:
            df = results.df_results
            if column in df.columns.to_list():
                row = 'Total'
            elif 'Load' in column:
                tmp = column.split(' ')
                row = ' '.join(tmp[-2:])
                column = ' '.join(tmp[:-2])
            else:
                if column == 'Energy Grid':
                    df = results.df_total
                    column = 'energyG'
                    row = 'Daily Total [Wh/day]'
            value = df.loc[row, column]
            l.append(value)
        self.df.loc[len(self.df)] = l