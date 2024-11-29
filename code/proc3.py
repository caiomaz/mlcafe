import pandas as pd
import time

def calcular_medias(caminho_csv, caminho_saida):
    """
    Calcula a média de colunas especificadas em um arquivo CSV, ignorando linhas com valores inválidos (-9999),
    e salva os resultados em outro CSV com formatação ajustada para separadores decimais e de milhar.

    Args:
        caminho_csv (str): Caminho completo do arquivo CSV de entrada.
        caminho_saida (str): Caminho completo do arquivo CSV de saída com os resultados.
    """
    # Lista de colunas para cálculo das médias
    colunas = [
        "PRECIPITACAO TOTAL, HORARIO (mm)",
        "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)",
        "PRESSAO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)",
        "PRESSAO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)",
        "RADIACAO GLOBAL (KJ/m2)",
        "TEMPERATURA DO AR - BULBO SECO, HORARIA (oC)",
        "TEMPERATURA DO PONTO DE ORVALHO (oC)",
        "TEMPERATURA MAXIMA NA HORA ANT. (AUT) (oC)",
        "TEMPERATURA MINIMA NA HORA ANT. (AUT) (oC)",
        "TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (oC)",
        "TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (oC)",
        "UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)",
        "UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)",
        "UMIDADE RELATIVA DO AR, HORARIA (%)",
        "VENTO, DIRECAO HORARIA (gr) (o (gr))",
        "VENTO, RAJADA MAXIMA (m/s)",
        "VENTO, VELOCIDADE HORARIA (m/s)"
    ]

    try:
        # Marcar o tempo inicial
        inicio = time.time()

        # Ler o arquivo CSV com tratamento de delimitador e valores inconsistentes
        try:
            dados = pd.read_csv(
                caminho_csv, 
                sep=';', 
                encoding="utf-8", 
                engine="python", 
                on_bad_lines="skip"
            )
        except UnicodeDecodeError:
            print("Tentando com a codificação 'ISO-8859-1'.")
            dados = pd.read_csv(
                caminho_csv, 
                sep=';', 
                encoding="ISO-8859-1", 
                engine="python", 
                on_bad_lines="skip"
            )

        # Substituir vírgulas por pontos para tratar valores numéricos
        dados.replace(',', '.', regex=True, inplace=True)

        # Garantir que as colunas sejam do tipo numérico
        for coluna in colunas:
            if coluna in dados.columns:
                dados[coluna] = pd.to_numeric(dados[coluna], errors="coerce")

        # Remover linhas com valor -9999 em qualquer uma das colunas de interesse
        dados_filtrados = dados
        for coluna in colunas:
            if coluna in dados_filtrados.columns:
                dados_filtrados = dados_filtrados[dados_filtrados[coluna] != -9999]

        # Verificar se as colunas especificadas existem no arquivo
        colunas_existentes = [col for col in colunas if col in dados_filtrados.columns]

        if not colunas_existentes:
            raise ValueError("Nenhuma das colunas especificadas foi encontrada no arquivo.")

        # Calcular a média de cada coluna presente
        medias = {}
        for coluna in colunas_existentes:
            medias[f"Média {coluna}"] = [dados_filtrados[coluna].mean()]

        # Criar um DataFrame com as médias
        df_medias = pd.DataFrame(medias)

        # Salvar o DataFrame em um novo arquivo CSV com formatação ajustada
        df_medias.to_csv(
            caminho_saida, 
            index=False, 
            encoding="utf-8", 
            sep=';', 
            decimal=','
        )
        print(f"Arquivo de médias gerado com sucesso: {caminho_saida}")

        # Marcar o tempo final e calcular a diferença
        fim = time.time()
        tempo_execucao = fim - inicio
        print("Tempo de execução:", tempo_execucao, "segundos")
    
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Exemplo de uso:
# Substitua os caminhos pelos caminhos do seu arquivo de entrada e saída.
caminho_csv = "../docs/varginha-geral.csv"  # Caminho do arquivo CSV de entrada
caminho_saida = "../docs/varginha-medias.csv"  # Caminho do arquivo CSV de saída

calcular_medias(caminho_csv, caminho_saida)
