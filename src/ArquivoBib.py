import pandas as pd
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

    def tratar_arquivo(self, df):
        # lowercase no nome de todos os campos
        df.columns = df.columns.str.lower()

        for coluna in df.columns:
            if coluna == "entrytype":
                df.rename(
                    columns={'entrytype': 'type_publication'},
                    inplace=True
                    )
                coluna = "type_publication"
                # print('Coluna renomeada')     

            if coluna not in self.lista_campos:
                df = df.drop(coluna, axis=1) # 0.linha 1.coluna

        #uppercase no campo Title
        df['title'] = df['title'].str.upper()

        return df  

    def remover_duplicados(self, df):
        print('Remover duplicados BIB - Antes: '); print(df.shape)
        df = df.drop_duplicates(inplace=False)
        print('Remover duplicados BIB - Depois: '); print(df.shape)

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
    def caminho(self):
        return self._caminho

    @property
    def lista_campos(self):
        return self._lista_campos        

