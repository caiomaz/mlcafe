import pandas as pd
import time

# Marcar o tempo inicial
inicio = time.time()

def processar_dados():
    try:
        # Carregar os dados das planilhas
        prod_cafe = pd.read_excel("../docs/prod-cafe-01.xlsx")
        cidades_mg = pd.read_excel("../docs/cidades-mg.xlsx")

        # Verificar colunas obrigatórias
        colunas_prod_cafe = {"Cidades", "Ano", "Produção (kg/ha)"}
        colunas_cidades_mg = {
            "Nome da Mesorregião",
            "Nome da Microrregião",
            "Município",
        }

        if not colunas_prod_cafe.issubset(prod_cafe.columns):
            raise ValueError(
                f"Colunas obrigatórias ausentes em 'prod-cafe-01.xlsx': {colunas_prod_cafe - set(prod_cafe.columns)}"
            )

        if not colunas_cidades_mg.issubset(cidades_mg.columns):
            raise ValueError(
                f"Colunas obrigatórias ausentes em 'cidades-mg.xlsx': {colunas_cidades_mg - set(cidades_mg.columns)}"
            )

        # Selecionar apenas as colunas relevantes de cidades_mg
        cidades_mg_relevantes = cidades_mg[
            ["Município", "Nome da Mesorregião", "Nome da Microrregião"]
        ]

        # Realizar a junção dos dados com base no município
        dados_combinados = pd.merge(
            prod_cafe,
            cidades_mg_relevantes,
            how="left",
            left_on="Cidades",  # Coluna do arquivo prod-cafe.xlsx
            right_on="Município",  # Coluna do arquivo cidades-mg.xlsx
        )

        # Preencher as colunas Mesorregiões e Microrregiões no arquivo original
        dados_combinados["Mesorregiões"] = dados_combinados["Nome da Mesorregião"]
        dados_combinados["Microrregiões"] = dados_combinados["Nome da Microrregião"]

        # Reorganizar as colunas para manter as originais e adicionar as novas
        dados_finais = dados_combinados[
            ["Cidades", "Mesorregiões", "Microrregiões", "Ano", "Produção (kg/ha)"]
        ]

        # Salvar o resultado em um arquivo Excel
        dados_finais.to_excel("../docs/prod-cafe-02.xlsx", index=False, engine="openpyxl")
        print("Arquivo 'prod-cafe-02.xlsx' gerado com sucesso.")

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Executar o processamento
processar_dados()

# Marcar o tempo final e calcular a diferença
fim = time.time()
tempo_execucao = fim - inicio

print("Tempo de execução:", tempo_execucao, "segundos")