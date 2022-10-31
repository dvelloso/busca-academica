import pandas as pd
import bibtexparser
import yaml
import os

class BuscaAcademica:
    
    def __init__(self):
        with open('configuracao/config.yaml', 'r') as f:
            try:
                self._arquivo_config = yaml.safe_load(f)
                self._lista_campos = self._arquivo_config['colunas']
                self._formato_arquivo = self._arquivo_config['formato_salvar_arquivo']
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
    

    