import csv
import os

def processar_varios_csv(arquivos_entrada, pasta_saida):
    """
    Processa múltiplos arquivos CSV para remover aspas e ajustar separadores, salvando os resultados em uma pasta de saída.

    Args:
        arquivos_entrada (list): Lista de caminhos dos arquivos de entrada.
        pasta_saida (str): Caminho da pasta onde os arquivos processados serão salvos.
    """
    try:
        # Criar a pasta de saída, se não existir
        os.makedirs(pasta_saida, exist_ok=True)

        for arquivo_entrada in arquivos_entrada:
            # Gerar o nome do arquivo de saída
            nome_arquivo = os.path.basename(arquivo_entrada)
            arquivo_saida = os.path.join(pasta_saida, nome_arquivo)

            with open(arquivo_entrada, 'r', encoding='utf-8') as infile, open(arquivo_saida, 'w', encoding='utf-8', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile, delimiter=';')

                for row in reader:
                    # Processar cada célula da linha
                    processed_row = []
                    for cell in row:
                        cell = cell.replace('"', '')  # Remover aspas
                        if cell.replace('.', '', 1).isdigit() or cell.replace(',', '', 1).isdigit():
                            cell = cell.replace('.', ',')  # Ajustar separadores decimais
                        processed_row.append(cell)

                    # Escrever a linha processada
                    writer.writerow(processed_row)

            print(f"Arquivo processado e salvo: {arquivo_saida}")

    except Exception as e:
        print(f"Erro ao processar os arquivos: {e}")

# Exemplo de uso:
arquivos_entrada = [
    '../docs/proc3-pre/input/2021/varginha.csv',
    '../docs/proc3-pre/input/2021/passos.csv',
    '../docs/proc3-pre/input/2021/caldas.csv',
    '../docs/proc3-pre/input/2021/passa-quatro.csv'
]
pasta_saida = '../docs/proc3-pre/output/2021'

processar_varios_csv(arquivos_entrada, pasta_saida)
