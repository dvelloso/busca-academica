from src.BuscaAcademica import BuscaAcademica

if __name__ == "__main__":
    busca = BuscaAcademica() 
    
    df_arq = busca.ler_arquivos()
        
    df_col = busca.definir_colunas(df_arq)

    busca.exportar_arquivo(df_col)
    print('Arquivo gerado com sucesso')