import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                             mean_absolute_percentage_error)
import matplotlib.pyplot as plt
import seaborn as sns

# Início da medição de tempo
start_time = time.time()

# Passo 1: Carregar os Dados
# Use CSV ou JSON conforme necessário
file_path = "../data/data.csv"  # Troque para "data.json" se for necessário
data = pd.read_csv(file_path)  # Para JSON, use: pd.read_json(file_path)

# Passo 2: Pré-processamento
# Converter colunas numéricas que estão em formato string (ex.: "0,1234" -> 0.1234)
for col in data.columns:
    if data[col].dtype == 'object':
        data[col] = data[col].str.replace(",", ".").astype(float, errors='ignore')

# Separar variáveis preditoras (X) e alvo (y)
X = data.drop(columns=["PRODUCAO"])  # Remove a variável alvo
y = data["PRODUCAO"]

# Codificar variáveis categóricas, se existirem
X = pd.get_dummies(X, drop_first=True)

# Passo 3: Divisão em Treinamento e Teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Passo 4: Treinamento do Modelo
model = LinearRegression()  # Instanciar o modelo de regressão linear
model.fit(X_train, y_train)  # Treinar o modelo

# Passo 5: Avaliação do Modelo
y_pred = model.predict(X_test)  # Prever os dados de teste

# Métricas de Avaliação
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

# Fim da medição de tempo
end_time = time.time()
execution_time = end_time - start_time

print(f"Tempo de execução: {execution_time} segundos")

print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"R²: {r2}")
print(f"MAPE: {mape}")

# Passo 6: Visualizações
# Gráfico de Resíduos
plt.figure(figsize=(10, 6))
residuos = y_test - y_pred
sns.scatterplot(x=y_pred, y=residuos)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Previsões')
plt.ylabel('Resíduos')
plt.title('Resíduos vs Previsões')
plt.show()

# Gráfico de Valores Reais vs Previstos
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Valores Reais')
plt.ylabel('Previsões')
plt.title('Valores Reais vs Previstos')
plt.show()

# Lista das variáveis de interesse
features_of_interest = [
    "ALTITUDE NO NIVEL DO MAR",
    "MEDIA DE PRECIPITACAO TOTAL",
    "MEDIA DE PRESSAO ATMOSFERICA",
    "MEDIA DE RADIACAO GLOBAL",
    "MEDIA DE TEMPERATURA DO AR",
    "MEDIA DE TEMPERATURA DO PONTO DE ORVALHO",
    "MEDIA DE UMIDADE RELATIVA DO AR",
    "MEDIA DE VELOCIDADE DO VENTO"
]

# Filtrar os coeficientes para essas variáveis
coeficientes = pd.Series(model.coef_, index=X.columns)
coeficientes = coeficientes[features_of_interest]

# Plotar a importância das variáveis
plt.figure(figsize=(10, 6))
coeficientes.sort_values().plot(kind='barh')
plt.title('Importância das Variáveis Selecionadas')
plt.xlabel('Coeficiente')
plt.ylabel('Variável')
plt.show()