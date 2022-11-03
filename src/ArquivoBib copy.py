import pandas as pd
import bibtexparser
import yaml
import os
import json

class ArquivoBib:
    
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

    # função para ler os arquivos
    def ler_arquivos(self):
        caminho = "dados/"
        dir = os.listdir(caminho)
        print(f'Arquivos listados no diretorio:  {dir}')   

        # df contendo todos os arquivos
        df_pai = pd.DataFrame()

        for arquivo in dir:
            with open(f'dados/{arquivo}', encoding='utf8') as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
                df = pd.DataFrame(bib_database.entries)
                #dfPai = pd.concat([dfPai, df])
                df_pai = df_pai.append(df)
            
        return df_pai

    def ler_arquivos_csv(self):
        caminho = 'dados/outros/'
        dir = os.listdir(caminho)
        print(f'Arquivos csv listados no diretorio: {dir}')

        df_pai = pd.DataFrame()

        # for arquivo in dir:
        for idx, val in enumerate(dir):
            df = pd.read_csv(f'{caminho}/{val}', sep=';', index_col=['Rank'] )
            df = self._tratar_arquivo_csv(df)
            if idx == 0:
                df_pai = df
            else:
                df_pai = pd.merge(df_pai, df, on='Title')
        
        return df_pai

    def _tratar_arquivo_csv(self, df):
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
        # eliminar os duplicados
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
        # df = df.query('Sourceid in [29431,20315]')

        return df


    def definir_colunas(self, df):
        for coluna in df.columns:
            if coluna == "ENTRYTYPE":
                df.rename(
                    columns={'ENTRYTYPE': 'type_publication'},
                    inplace=True
                    )
                coluna = "type_publication"
                print('Coluna renomeada')     

            if coluna not in self.lista_campos:
                df = df.drop(coluna, axis=1) # 0.linha 1.coluna
                #print(f'Coluna excluida: {coluna}')  

        return df  

    def exportar_arquivo(self, df):
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
            arq = open(f'resultados/arquivo.{self.formato_arquivo}', 'w', encoding='utf-8')
            arq.write(df)
            arq.close

    @property
    def lista_campos(self):
        return self._lista_campos        

    @property
    def arquivo_config(self):
        return self._arquivo_config

    @property
    def formato_arquivo(self):
        return self._formato_arquivo
    
    @property
    def filtros(self):
        return self._filtros
    