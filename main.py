from src.ArquivoCSV import ArquivoCSV
from src.BuscaAcademica import BuscaAcademica


if __name__ == "__main__":
    
    busca = BuscaAcademica()
    df_csv =  busca.executar_csv()
    busca.exportar_arquivo(df_csv, '_csv')
    df_bib = busca.executar_bib()
    busca.exportar_arquivo(df_bib, '_bib')
    df_unificado = busca.executar_unificado(df_csv, df_bib)

    busca.exportar_arquivo(df_unificado, '_final')
   