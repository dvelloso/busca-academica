import pandas as pd
import numpy as np
import bibtexparser
import yaml
import os
import json

class ArquivoBib:
    
    def __init__(self, lista_campos):
        self._caminho = 'dados/BIB/'
        self._lista_campos = lista_campos

    def ler_arquivo(self, nome_arquivo):
        with open(f'{self.caminho}{nome_arquivo}', encoding='utf8') as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
                df = pd.DataFrame(bib_database.entries)

        return df

    def unificar_arquivos(self, dfs):
        df_pai = pd.DataFrame()

        for df in dfs:
            # df_pai = df_pai.append(df) # depreciado
            df_pai = pd.concat([df_pai, df])

        return df_pai

    def tratar_arquivo(self, df, nome_arquivo):
        
        # lowercase no nome de todos os campos
        df.columns = df.columns.str.lower()

        for coluna in df.columns:
            if coluna == "entrytype":
                df.rename(
                    columns={'entrytype': 'type_publication'},
                    inplace=True
                    )
                coluna = "type_publication"

            if coluna == 'publication_year':
                df.rename(
                    columns={'publication_year': 'year'},
                    inplace=True
                    )
                coluna = "year"

            if coluna not in self.lista_campos:
                df = df.drop(coluna, axis=1) # 0.linha 1.coluna

        #uppercase no campo Title
        df['title'] = df['title'].str.upper()

        # issn: tirar caracter '-'
        if 'issn' in df.columns:
            df['issn'] = df['issn'].map(lambda x: x.replace('-','') if x == x else np.nan)

        return df  

    def remover_duplicados(self, df):
        print('Remover duplicados BIB - Antes: '); print(df.shape)
        df = df.drop_duplicates(inplace=False)
        print('Remover duplicados BIB - Depois: '); print(df.shape)

        return df              

    @property
    def caminho(self):
        return self._caminho

    @property
    def lista_campos(self):
        return self._lista_campos        

