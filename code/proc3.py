import pandas as pd
import os
import time

def calcular_medias_varios_csv(arquivos_entrada, pasta_saida):
    """
    Calcula as médias de colunas especificadas para múltiplos arquivos CSV e salva os resultados na pasta de saída.

    Args:
        arquivos_entrada (list): Lista de caminhos dos arquivos de entrada.
        pasta_saida (str): Caminho da pasta onde os arquivos processados serão salvos.
    """
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
        "UMIDADE RELATIVA DO AR, HORARIA (%)",
        "VENTO, DIRECAO HORARIA (gr) (o (gr))",
        "VENTO, VELOCIDADE HORARIA (m/s)"
    ]

    try:
        # Criar a pasta de saída, se não existir
        os.makedirs(pasta_saida, exist_ok=True)

        for arquivo_entrada in arquivos_entrada:
            inicio = time.time()
            nome_arquivo = os.path.basename(arquivo_entrada)
            arquivo_saida = os.path.join(pasta_saida, f"medias-{nome_arquivo}")

            try:
                dados = pd.read_csv(arquivo_entrada, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
            except UnicodeDecodeError:
                dados = pd.read_csv(arquivo_entrada, sep=';', encoding='ISO-8859-1', engine='python', on_bad_lines='skip')

            dados.replace(',', '.', regex=True, inplace=True)

            for coluna in colunas:
                if coluna in dados.columns:
                    dados[coluna] = pd.to_numeric(dados[coluna], errors='coerce')

            dados_filtrados = dados
            for coluna in colunas:
                if coluna in dados_filtrados.columns:
                    dados_filtrados = dados_filtrados[dados_filtrados[coluna] != -9999]

            colunas_existentes = [col for col in colunas if col in dados_filtrados.columns]
            medias = {f"Média {col}": [dados_filtrados[col].mean()] for col in colunas_existentes}

            df_medias = pd.DataFrame(medias)
            df_medias.to_csv(arquivo_saida, index=False, encoding='utf-8', sep=';', decimal=',')

            fim = time.time()
            print(f"Arquivo de médias salvo: {arquivo_saida} (Tempo: {fim - inicio:.2f} segundos)")

    except Exception as e:
        print(f"Erro ao processar os arquivos: {e}")

# Exemplo de uso:
arquivos_entrada = [
    "../docs/proc3-pre/output/2021/varginha.csv",
    "../docs/proc3-pre/output/2021/passos.csv",
    "../docs/proc3-pre/output/2021/caldas.csv",
    "../docs/proc3-pre/output/2021/passa-quatro.csv"
]
pasta_saida = "../docs/proc4/input/2021"

calcular_medias_varios_csv(arquivos_entrada, pasta_saida)
