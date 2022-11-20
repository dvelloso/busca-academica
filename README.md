# busca-academica
Projeto desenvolvido na aula de Python no curso de Engenharia de Dados

Processos
---------
- 1º passo
    - Ler e unificar arquivos do diretório /dados/BIB   
    - Validação de dados
    - Arquivo final deve conter apenas os campos definidos no arquivo Yaml de configuração
    - Exportar para os formatos CSV, Json, Xml, Yaml

- 2º passo
    - Ler e unificar arquivos do diretório /dados/CSV
    - Validação de dados
    - Fazer join com o arquivo .BIB definido no 1º passo
    - Configuração de filtro definida no arquivo Yaml

- 3º passo
    - Criar API de integração com ieeexploreapi.ieee.org/api/v1/search/articles
    - Definir filtro de pesquisa no arquivo Yaml a ser usado na API
    - Agrupar o retorno da api acima nos arquivos .BIB
    - Fazer join com os arquivos CSV do 2º passo
    - Gravar resultado em banco de dados

Libs Utilizadas
--------------
- Pandas
- Numpy
- BibtexParser
- PyYAML
- Json
- Requests
- Math


