import pandas as pd
import time

def calcular_media_entre_planilhas(caminho_csv1, caminho_csv2, caminho_saida):
    """
    Calcula a média das colunas entre duas planilhas de médias e salva o resultado em um novo arquivo CSV.

    Args:
        caminho_csv1 (str): Caminho do primeiro arquivo CSV.
        caminho_csv2 (str): Caminho do segundo arquivo CSV.
        caminho_saida (str): Caminho do arquivo CSV de saída com as médias.
    """
    try:
        # Marcar o tempo inicial
        inicio = time.time()

        # Ler as duas planilhas de médias
        dados1 = pd.read_csv(caminho_csv1, sep=";", encoding="utf-8", decimal=",")
        dados2 = pd.read_csv(caminho_csv2, sep=";", encoding="utf-8", decimal=",")

        # Verificar se as colunas das duas planilhas são iguais
        if not dados1.columns.equals(dados2.columns):
            raise ValueError("As colunas das duas planilhas não são iguais.")

        # Criar um novo DataFrame para armazenar as médias
        medias_totais = {}

        # Calcular a média entre as duas planilhas para cada coluna
        for coluna in dados1.columns:
            if coluna != "Média":  # Ignorar se existir uma coluna não numérica como índice
                medias_totais[f"{coluna} Total"] = (dados1[coluna] + dados2[coluna]) / 2

        # Criar um DataFrame com as médias
        df_medias_totais = pd.DataFrame(medias_totais)

        # Salvar o DataFrame de médias em um novo arquivo CSV
        df_medias_totais.to_csv(
            caminho_saida,
            index=False,
            encoding="utf-8",
            sep=";",
            decimal=","
        )

        print(f"Arquivo de médias 'Total' gerado com sucesso: {caminho_saida}")

        # Marcar o tempo final e calcular a diferença
        fim = time.time()
        tempo_execucao = fim - inicio
        print("Tempo de execução:", tempo_execucao, "segundos")
    
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Exemplo de uso:
# Substitua os caminhos pelos caminhos dos seus arquivos de entrada e saída.
caminho_csv1 = "../docs/medias-passos.csv"  # Caminho do primeiro arquivo CSV de médias
caminho_csv2 = "../docs/medias-varginha.csv"  # Caminho do segundo arquivo CSV de médias
caminho_saida = "../docs/medias-total.csv"  # Caminho do arquivo CSV de saída com as médias totais

calcular_media_entre_planilhas(caminho_csv1, caminho_csv2, caminho_saida)
