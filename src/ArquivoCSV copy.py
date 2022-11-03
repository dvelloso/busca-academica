import pandas as pd
import yaml
import os
import json

class ArquivoCSV:
    
    def __init__(self):
        with open('configuracao/config.yaml', 'r') as f:
            try:
                self._arquivo_config = yaml.safe_load(f)
                self._filtros = self._arquivo_config['filtros']
                print(f'Parâmetros configuração: {self._arquivo_config}')
            except yaml.YAMLError as exc:
                print(exc)   

    def ler_arquivos(self):
        caminho = 'dados/CSV/'
        dir = os.listdir(caminho)
        print(f'Arquivos csv listados no diretorio: {dir}')

        df_pai = pd.DataFrame()

        # for arquivo in dir:
        for idx, val in enumerate(dir):
            df = pd.read_csv(f'{caminho}/{val}', sep=';', index_col=['Rank'] )
            df = self._tratar_arquivo(df)
            if idx == 0:
                df_pai = df
            else:
                df_pai = pd.merge(df_pai, df, on='Title')
        
        return df_pai

    def _tratar_arquivo(self, df):
        #eliminar coluna com nulos
        df = df.dropna(axis=1, how='all')
        
        for coluna in df.columns:
            if coluna == 'Full Journal Title':
                #alterar nome da coluna
                df = df.rename(columns={'Full Journal Title':'Title'}, inplace=False)

            #uppercase no campo Title
            df['Title'] = df['Title'].str.upper()

        return df

    def remover_duplicados(self, df):
        print(df.shape)
        df = df.drop_duplicates(inplace=False)
        print(df.shape)

        return df

    def filtrar(self, df):
        dict_filtro = json.loads(self.filtros)
        filtro_query = '###'
        for filtro in dict_filtro.keys():
            print(filtro, " = ", dict_filtro[filtro])
            if filtro == 'Sourceid':
                filtro_query = f'{filtro_query} & Sourceid in {dict_filtro[filtro]}' 
            elif filtro == 'Type':
                filtro_query = f'{filtro_query} & Type in {dict_filtro[filtro]}'

        filtro_query = filtro_query.replace('### &','')
        print(filtro_query)    
        df = df.query(filtro_query)

        return df

    @property
    def filtros(self):
        return self._filtros
