import requests
import pandas as pd
import yaml
import math

class ApiIEEE: 

    def __init__(self):
        self._limite_registros_por_pagina = 200

        with open('configuracao/config.yaml', 'r') as f:
            try:
                self._arquivo_config = yaml.safe_load(f)
                self._total_consultas = self._arquivo_config['api']['total_consultas']
                self._filtro = self._arquivo_config['api']['filtro']
                self._url = self._arquivo_config['api']['ieee']['url'] + '&querytext=' + self._filtro

                print(f'Parâmetros configuração ApiIEEE: {self._url}')
            except yaml.YAMLError as exc:
                print(exc)      

    def get_numero_consultas(self, total_registros):
        return math.ceil(total_registros/self._limite_registros_por_pagina)

    def get_url_tratada(self, numero_consulta):
        return self._url + f'&start_record={numero_consulta}'


    def pesquisar_artigos(self):
        df_pai = pd.DataFrame()

        # 1ª consulta
        url = self.get_url_tratada(1)
        r = requests.get(url)

        if r.status_code != 200:
            raise Exception('Erro ao pesquisar artigos.')
        
        total_registros = r.json()['total_records']
        numero_consultas = self.get_numero_consultas(total_registros)
        print(f'API-IEEE->0/{numero_consultas}-{url}')

        dict_df = r.json()
        dict_df = dict_df['articles']
        df_pai = pd.json_normalize(data=dict_df)

        for numero_consulta in range(numero_consultas):
            # a partir da 2ª consulta
            if numero_consulta > 0:

                if numero_consulta == self._total_consultas:
                    break

                start_record = 1 + (numero_consulta*200)
                url = self.get_url_tratada(start_record)
                print(f'API-IEEE->{numero_consulta}/{numero_consultas}-{url}')

                r = requests.get(url)
                dict_df = r.json()
                dict_df = dict_df['articles']
                df = pd.json_normalize(data=dict_df)

                df_pai = pd.concat([df_pai, df])
        
        return df_pai
    
