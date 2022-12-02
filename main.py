from src.ArquivoCSV import ArquivoCSV
from src.BuscaAcademica import BuscaAcademica
import sqlite3

if __name__ == "__main__":
    
    busca = BuscaAcademica()

    # arquivos CSV
    df_csv =  busca.executar_csv()
    busca.exportar_arquivo(df_csv, '_csv')

    # arquivos BIB
    df_bib = busca.executar_bib()
    busca.exportar_arquivo(df_bib, '_bib')

    # api bib IEEE
    df_api_ieee = busca.executar_api_ieee()
    busca.exportar_arquivo(df_api_ieee, '_bib_apiieee')

    # unificar arquivos bib com api bib IEEE
    df_unificado_bib_api = busca.unificar_arquivos_bib([df_bib,df_api_ieee])
    busca.exportar_arquivo(df_unificado_bib_api, '_bib_unificado_api')

    # unificar arquivos
    df_unificado = busca.executar_unificado(df_csv, df_unificado_bib_api)

    # exportar
    busca.exportar_arquivo(df_unificado, '_final')

    # gravar resultado em banco de dados
    busca.gravar_resultado_bd(df_unificado)