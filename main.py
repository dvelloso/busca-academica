import pandas as pd
import bibtexparser
import yaml
import os

# ler arquivo yaml
with open('config.yaml', 'r') as f:
    try:
        arquivo_config = yaml.safe_load(f)
        print(f'Parâmetros configuração: {arquivo_config}')
    except yaml.YAMLError as exc:
        print(exc)

# função para ler os arquivos
def ler_arquivos():
  caminho = "dados/"
  dir = os.listdir(caminho)
  print(f'Arquivos listados no diretorio:  {dir}')   

  # df contendo todos os arquivos
  dfPai = pd.DataFrame()

  for arquivo in dir:
    with open(f'dados/{arquivo}', encoding='utf8') as bibtex_file:
      bib_database = bibtexparser.load(bibtex_file)
      df = pd.DataFrame(bib_database.entries)
      #dfPai = pd.concat([dfPai, df])
      dfPai = dfPai.append(df)
      
  return dfPai

def definir_colunas(df):
  for coluna in df.columns:
    if coluna not in LISTA_CAMPOS:
      df = df.drop(coluna, axis=1) # 0.linha 1.coluna
      #print(f'Coluna excluida: {coluna}')  

  return df  

def exportar_arquivo(df, formato):
  formatoValido = False
  if formato == 'json':
    df = df.to_json(orient='split')
    formatoValido = True

  if formatoValido:
    arq = open(f'resultados/arquivo.{formato}', 'w', encoding='utf-8')
    arq.write(df)
    arq.close
   
if __name__ == "__main__":
  # constantes
  LISTA_CAMPOS = arquivo_config['colunas']
  FORMATO_ARQUIVO = arquivo_config['formato_salvar_arquivo']

  dfArq = ler_arquivos()

  dfCol = definir_colunas(dfArq)

  exportar_arquivo(dfCol, FORMATO_ARQUIVO)
  print('Arquivo gerado com sucesso')