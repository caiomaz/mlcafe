import pandas as pd
import time

def converter_csv_para_xlsx(caminho_csv, caminho_xlsx):
    """
    Converte um arquivo CSV para o formato XLSX.
    
    Args:
        caminho_csv (str): Caminho completo do arquivo .csv de entrada.
        caminho_xlsx (str): Caminho completo para salvar o arquivo .xlsx de saída.
    """
    try:
        # Marcar o tempo inicial
        inicio = time.time()

        # Ler o arquivo CSV com tentativa de codificação robusta
        try:
            dados = pd.read_csv(caminho_csv, encoding="utf-8")
        except UnicodeDecodeError:
            print("Aviso: Codificação 'utf-8' falhou. Tentando 'ISO-8859-1'.")
            dados = pd.read_csv(caminho_csv, encoding="ISO-8859-1")

        # Salvar o arquivo no formato XLSX
        dados.to_excel(caminho_xlsx, index=False, engine="openpyxl")
        print(f"Arquivo convertido com sucesso: {caminho_xlsx}")

        # Marcar o tempo final e calcular a diferença
        fim = time.time()
        tempo_execucao = fim - inicio
        print("Tempo de execução:", tempo_execucao, "segundos")
    
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Exemplo de uso:
# Substitua os caminhos pelos caminhos do seu arquivo de entrada e saída.
caminho_csv = "../docs/VARGINHA-2012.csv"  # Caminho do arquivo CSV
caminho_xlsx = "../docs/VARGINHA-2012.xlsx"  # Caminho do arquivo XLSX de saída

converter_csv_para_xlsx(caminho_csv, caminho_xlsx)
