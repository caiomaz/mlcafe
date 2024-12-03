import pandas as pd
import time
import os

def calcular_media_entre_varias_planilhas(caminhos_csv, caminho_saida):
    """
    Calcula a média das colunas entre várias planilhas e salva o resultado em um novo arquivo CSV.

    Args:
        caminhos_csv (list): Lista de caminhos dos arquivos CSV.
        caminho_saida (str): Caminho do diretório de saída.
    """
    try:
        # Marcar o tempo inicial
        inicio = time.time()

        # Verificar se há arquivos suficientes
        if len(caminhos_csv) < 2:
            raise ValueError("É necessário pelo menos dois arquivos para calcular as médias.")

        # Criar diretório de saída, se não existir
        os.makedirs(caminho_saida, exist_ok=True)

        # Ler todas as planilhas
        dados_lista = [pd.read_csv(caminho, sep=";", encoding="utf-8", decimal=",") for caminho in caminhos_csv]

        # Verificar se todas as planilhas têm as mesmas colunas
        colunas_comuns = dados_lista[0].columns
        for i, dados in enumerate(dados_lista[1:], start=2):
            if not colunas_comuns.equals(dados.columns):
                raise ValueError(f"As colunas da planilha {i} não correspondem às da primeira planilha.")

        # Calcular a média entre todas as planilhas
        df_medias_totais = sum(dados_lista) / len(dados_lista)

        # Adicionar " Total" ao nome das colunas
        df_medias_totais.columns = [f"{coluna} Total" for coluna in df_medias_totais.columns]

        # Salvar o DataFrame em um novo arquivo CSV
        caminho_saida_arquivo = os.path.join(caminho_saida, "medias-totais.csv")
        df_medias_totais.to_csv(
            caminho_saida_arquivo,
            index=False,
            encoding="utf-8",
            sep=";",
            decimal=","
        )
        print(f"Arquivo de médias 'Total' gerado com sucesso: {caminho_saida_arquivo}")

        # Marcar o tempo final e calcular a diferença
        fim = time.time()
        tempo_execucao = fim - inicio
        print("Tempo de execução:", tempo_execucao, "segundos")
    
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Exemplo de uso:
caminhos_csv = [
    "../docs/proc4/input/2021/medias-caldas.csv",
    "../docs/proc4/input/2021/medias-passos.csv",
    "../docs/proc4/input/2021/medias-varginha.csv",
    "../docs/proc4/input/2021/medias-passa-quatro.csv"
]
caminho_saida = "../docs/proc4/output/2021"

calcular_media_entre_varias_planilhas(caminhos_csv, caminho_saida)
