import pandas as pd
import time


# Marcar o tempo inicial
inicio = time.time()


def processar_dados():
    try:
        # Carregar os dados das planilhas
        prod_cafe = pd.read_excel("../docs/prod-cafe.xlsx")
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
                f"Colunas obrigatórias ausentes em 'prod-cafe.xlsx': {colunas_prod_cafe - set(prod_cafe.columns)}"
            )

        if not colunas_cidades_mg.issubset(cidades_mg.columns):
            raise ValueError(
                f"Colunas obrigatórias ausentes em 'cidades-mg.xlsx': {colunas_cidades_mg - set(cidades_mg.columns)}"
            )

        # Renomear colunas para uniformizar
        prod_cafe.rename(columns={"Cidades": "Município"}, inplace=True)

        # Selecionar apenas as colunas relevantes de cidades_mg
        cidades_mg_relevantes = cidades_mg[
            ["Município", "Nome da Mesorregião", "Nome da Microrregião"]
        ]

        # Realizar a junção dos dados com base no município
        dados_combinados = pd.merge(
            prod_cafe, cidades_mg_relevantes, how="left", on="Município"
        )

        # Renomear colunas no resultado final
        dados_combinados.rename(
            columns={
                "Nome da Mesorregião": "Mesorregiões",
                "Nome da Microrregião": "Microrregiões",
            },
            inplace=True,
        )

        # Reorganizar as colunas conforme o requisito
        dados_finais = dados_combinados[
            ["Municípios", "Mesorregiões", "Microrregiões", "Ano", "Produção (kg/ha)"]
        ]

        # Salvar o resultado em um arquivo CSV
        dados_finais.to_csv("prod-cafe-atualizado.csv", index=False, encoding="utf-8")
        print("Arquivo 'prod-cafe-atualizado.csv' gerado com sucesso.")

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")


# Executar o processamento
processar_dados()


# Marcar o tempo final e calcular a diferença
fim = time.time()
tempo_execucao = fim - inicio

print("Tempo de execução:", tempo_execucao, "segundos")
