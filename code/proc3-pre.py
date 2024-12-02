import csv

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, delimiter=';')
        
        for row in reader:
            # Remover aspas em cada célula e ajustar o formato
            processed_row = []
            for cell in row:
                # Remover aspas
                cell = cell.replace('"', '')
                
                # Substituir "." por "," em valores decimais
                if cell.replace('.', '', 1).isdigit() or cell.replace(',', '', 1).isdigit():
                    cell = cell.replace('.', ',')
                
                processed_row.append(cell)
            
            # Escrever a linha processada no novo arquivo
            writer.writerow(processed_row)

# Arquivo de entrada e saída
input_file = '../docs/proc3-pre/input/2012/passa-quatro.csv'  # Substitua pelo caminho do seu arquivo de entrada
output_file = '../docs/proc3-pre/output/2012/passa-quatro.csv'  # Substitua pelo caminho do arquivo de saída

# Processar o arquivo
process_csv(input_file, output_file)
