from src.ArquivoCSV import ArquivoCSV
from src.ArquivoBib import ArquivoBib
import os
import pandas as pd
import json
import yaml

class BuscaAcademica:

    def __init__(self):
        with open('configuracao/config.yaml', 'r') as f:
            try:
                self._arquivo_config = yaml.safe_load(f)
                self._lista_campos = self._arquivo_config['colunas']
                self._formato_arquivo = self._arquivo_config['formato_salvar_arquivo']
                self._filtros = self._arquivo_config['filtros']
                print(f'Parâmetros configuração: {self._arquivo_config}')
            except yaml.YAMLError as exc:
                print(exc)  

    def executar_csv(self):
        
        arq_csv = ArquivoCSV()

        dir = os.listdir('dados/CSV/')
        print(f'Arquivos CSV listados no diretorio: {dir}')

        lista_df_csv_tratados = []
        # ler e tratar os arquivos
        for idx, val in enumerate(dir):
            print(f'Lendo arquivo: dados/CSV/{val} - {idx}')
            df_tratado = arq_csv.tratar_arquivo(arq_csv.ler_arquivo(val), val)
            lista_df_csv_tratados.append(df_tratado)

        # unificar arquivos
        df_unificado = arq_csv.unificar_arquivos(lista_df_csv_tratados)
        # print('df_csv_unificado'); print(df_unificado.head)

        df_unificado = arq_csv.remover_duplicados(df_unificado)
        print('df_csv_unificado removido duplicadas'); print(df_unificado.head); 
        
        return df_unificado

    def executar_bib(self):
        arq_bib = ArquivoBib(self.lista_campos)

        dir_bib = ('ACM','IEEE','SDC')
        lista_df_bib_tratados = []
        for x in dir_bib:
            dir = os.listdir(f'dados/BIB/{x}/')
            print(f'Arquivos bib listados no diretorio {x}: {dir}')

            # ler arquivos
            for idx, val in enumerate(dir):
                print(f'Lendo arquivo: dados/BIB/{val} - {idx}')
                df_tratado =  arq_bib.tratar_arquivo(arq_bib.ler_arquivo(f'{x}/{val}'), val)
                lista_df_bib_tratados.append(df_tratado)

        # unificar arquivos
        df_unificado = arq_bib.unificar_arquivos(lista_df_bib_tratados)

        df_unificado = arq_bib.remover_duplicados(df_unificado)

        print('df_csv_unificado removido duplicadas'); print(df_unificado)

        return df_unificado

    def executar_unificado(self, df_csv, df_bib):
        print('df_unificado_csv -> '); print(df_csv)
        print('df_unificado_bib -> ');print(df_bib)

        df_unificado_csv_bib = pd.merge(df_csv, df_bib, on='issn')

        df_unificado_csv_bib.drop_duplicates(inplace=True)

        df_unificado_csv_bib.rename(columns={'title_x':'title_csv'}, inplace=True)
        df_unificado_csv_bib.rename(columns={'title_y':'title_bib'}, inplace=True)

        print('df_unificado_bib_csv -> '); print(df_unificado_csv_bib)

        return df_unificado_csv_bib

    def filtrar(self, df):
        dict_filtro = json.loads(self.filtros)
        filtro_query = '###'
        for filtro in dict_filtro.keys():
            print(filtro, " = ", dict_filtro[filtro])
            if filtro == 'sourceid':
                filtro_query = f'{filtro_query} & sourceid in {dict_filtro[filtro]}' 
            elif filtro == 'title':               
                filtro_query = f'{filtro_query} & title in {dict_filtro[filtro]}'
            elif filtro == 'abstract':               
                filtro_query = f'{filtro_query} & abstract in {dict_filtro[filtro]}'
            elif filtro == 'year':               
                filtro_query = f'{filtro_query} & year in {dict_filtro[filtro]}'
            elif filtro == 'type_publication':               
                filtro_query = f'{filtro_query} & type_publication in {dict_filtro[filtro]}'
            elif filtro == 'doi':               
                filtro_query = f'{filtro_query} & doi in {dict_filtro[filtro]}'
            else:
                raise Exception('Filtro não disponível.')

        filtro_query = filtro_query.replace('### &','')
        print(filtro_query)    
        df = df.query(filtro_query, inplace=False)

        return df

    def exportar_arquivo(self, df, tipo):
        formato_valido = False
        if self.formato_arquivo == 'json':
            df = df.to_json(orient='split')
            formato_valido = True
        elif self.formato_arquivo == 'csv':
            df = df.to_csv()
            formato_valido = True
        elif self.formato_arquivo == 'yaml':
            df = yaml.dump(df.reset_index().to_dict(orient='records'),
                sort_keys=False, width=72, indent=4,
                default_flow_style=None)
            formato_valido = True           
        elif self.formato_arquivo == 'xml':
            df = df.to_xml(root_name='bib', row_name='paper')
            formato_valido = True

        if formato_valido:
            arq = open(f'resultados/arquivo{tipo}.{self.formato_arquivo}', 'w', encoding='utf-8')
            arq.write(df)
            arq.close

    @property
    def arquivo_config(self):
        return self._arquivo_config

    @property
    def formato_arquivo(self):
        return self._formato_arquivo
    
    @property
    def filtros(self):
        return self._filtros

    @property
    def lista_campos(self):
        return self._lista_campos     