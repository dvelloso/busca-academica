import pandas as pd
import numpy as np
import yaml
import os
import json

class ArquivoCSV:
    
    def __init__(self):
        self._caminho = 'dados/CSV/'

    def ler_arquivo(self, nome_arquivo):
        df = pd.read_csv(f'{self.caminho}/{nome_arquivo}', sep=';', index_col=['Rank'], low_memory=False )
        
        return df

    def unificar_arquivos(self, dfs):
        df_pai = pd.DataFrame()

        for idx, df in enumerate(dfs):
            if idx == 0:
                df_pai = df
            else:
                df_pai = pd.merge(df_pai, df, on='title')

        return df_pai

    def tratar_arquivo(self, df, nome_arquivo):

        #eliminar coluna com nulos
        df = df.dropna(axis=1, how='all')

        # lowercase no nome de todos os campos
        df.columns = df.columns.str.lower()    
        
        for coluna in df.columns:
            if coluna == 'full journal title':
                #alterar nome da coluna
                df = df.rename(columns={'full journal title':'title'}, inplace=False)

        #uppercase no campo Title
        df['title'] = df['title'].str.upper()

        # issn: transformar em lista e quebrar em linhas
        if 'issn' in df.columns:
            df['issn'] = df['issn'].apply(lambda x: x.split(', ') if x==x else np.nan)
            df = df.explode('issn')

        return df

    def remover_duplicados(self, df):
        print('Remover duplicados CSV - Antes: '); print(df.shape)
        df = df.drop_duplicates(inplace=False)
        print('Remover duplicados CSV - Depois: ');print(df.shape)

        return df

    @property
    def caminho(self):
        return self._caminho