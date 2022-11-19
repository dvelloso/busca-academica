import requests
import pandas as pd
import yaml

class ApiIEEE: 

    def __init__(self):
        with open('configuracao/config.yaml', 'r') as f:
            try:
                self._arquivo_config = yaml.safe_load(f)
                self._filtro = self._arquivo_config['api']['filtro']
                self._url = self._arquivo_config['api']['ieee']['url'] + '&querytext=' + self._filtro

                print(f'Parâmetros configuração ApiIEEE: {self._url}')
            except yaml.YAMLError as exc:
                print(exc)      

    def pesquisar_artigos(self):
        df_pai = pd.DataFrame()

        #  TODO refatorar criar metodo para requests
        url = self._url + '&start_record=1'
        r = requests.get(url)
        print(f'API-IEEE -> 1 - {url}')
        if r.status_code != 200:
            raise Exception('Erro ao pesquisar artigos.')
        
        total_registros = r.json()['total_records']
        dict_df = r.json()
        dict_df = dict_df['articles']
        df_pai = pd.json_normalize(data=dict_df)

        i = 2
        qtd = 1
        while i != 5: # TODO validar total de registros
            qtd = qtd + 200 
            url = self._url + '&start_record=' + str(qtd)
            r = requests.get(url)
            print(f'API-IEEE -> {i} - {url}')
            dict_df = r.json()
            dict_df = dict_df['articles']
            df = pd.json_normalize(data=dict_df)

            df_pai = pd.concat([df_pai, df])
            
            i = i+1

        return df_pai
    
