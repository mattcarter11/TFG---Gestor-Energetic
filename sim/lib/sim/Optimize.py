import pandas as pd
from .Results import Results

class Optimize:

    def __init__(self, index_name:str, columns:dict[str:dict[str:str, str:str, str:str]]):
        columns.pop('None')
        self.columns = columns
        self.df = pd.DataFrame(columns=[index_name]+list(columns.keys()))

    def add_results(self, index:int, results:Results):
        l = [index]
        for _, item in self.columns.items():
            match item['table']:
                case 'results':
                    df = results.df_results
                case 'total':
                    df = results.df_total
            l.append(df.loc[item['row'], item['column']])
        self.df.loc[len(self.df)] = l