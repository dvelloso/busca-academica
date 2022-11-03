from src.ArquivoCSV import ArquivoCSV
from src.BuscaAcademica import BuscaAcademica


if __name__ == "__main__":
    
    s = '******************************************************************'

    busca = BuscaAcademica()
    df_csv =  busca.executar_csv()
    df_bib = busca.executar_bib()
    df_unificado = busca.executar_unificado(df_csv, df_bib)

    print(s)
    print('df Antes do filtro'); print(df_unificado)
    print(s)
    df_unificado = busca.filtrar(df_unificado)
    print(s)
    print('df apos filtro'); print(df_unificado)    
    print(s)

    busca.exportar_arquivo(df_unificado)
    