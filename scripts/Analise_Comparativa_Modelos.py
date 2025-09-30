# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
#
# # Análise Comparativa de Modelos de Previsão - Com e Sem Lag-Features
#  
# O notebook apresenta uma análise comparativa sistemática dos modelos de machine learning para previsão de dados meteorológicos.
#  
# ## Estrutura:
# 1. Preparação do Ambiente e Dados
# 2. Criação dos Datasets
# 3. Avaliação dos Modelos
# 4. Comparação Final e Conclusões
#
# ## Preparação do Ambiente e Dados
#  
# ### Importação das Bibliotecas

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# %% [markdown]
# ### 1.2 Carregamento dos Dados

# %%
# Definição das colunas do dataset
colunas = [
    "data",
    "precipitacao_total",
    "pressao_atm_media",
    "temp_orvalho_media",
    "temp_maxima",
    "temp_media",
    "temp_minima",
    "umidade_relativa_media",
    "umidade_relativa_minima",
    "umidade_relativa_maxima",
    "vento_vel_media",
]

# Carregamento dos dados
caminho_csv = "/home/iioulos/Documents/IC_Danilo-Cotozika/Dados do INEP que eu solicitei/dados_A707_D_2014-01-01_2025-05-01.csv"
df = pd.read_csv(
    caminho_csv, sep=",", encoding="latin1", skiprows=11, header=None, names=colunas
)

# Verificação de valores faltantes
print("Valores faltantes por coluna:")
df.isna().sum()

# %% [markdown]
# ### 1.3 Tratamento de Dados

# %%
# Convertendo a coluna de data para datetime
df["data"] = pd.to_datetime(df["data"])

# Interpolação linear para valores faltantes
colunas_numericas = df.select_dtypes(include=[np.number]).columns
df[colunas_numericas] = df[colunas_numericas].interpolate(method="linear")

print("\nValores faltantes após interpolação:")
df.isna().sum()


# %% [markdown]
# ## 2. Criação dos Datasets
#  
# ### 2.1 Dataset sem Lag-Features
#

# %%
def preparar_dataset_sem_lag(df):
    """
    Prepara o dataset sem utilizar lag-features.
    """
    X = df[
        [
            "pressao_atm_media",
            "temp_orvalho_media",
            "umidade_relativa_media",
            "umidade_relativa_minima",
            "umidade_relativa_maxima",
            "vento_vel_media",
        ]
    ]
    y = df["temp_maxima"]

    return train_test_split(X, y, test_size=0.2, random_state=42)


# Preparando dados sem lag
X_train_sem_lag, X_test_sem_lag, y_train_sem_lag, y_test_sem_lag = (
    preparar_dataset_sem_lag(df)
)


# %% [markdown]
# ### 2.2 Dataset com Lag-Features

# %%
def criar_lag_features(df, lag_dias=[1, 2, 3, 7]):
    """
    Cria lag features para as variáveis selecionadas.
    """
    df_com_lag = df.copy()

    features_para_lag = [
        "temp_maxima",
        "pressao_atm_media",
        "temp_orvalho_media",
        "umidade_relativa_media",
        "vento_vel_media",
    ]

    for feature in features_para_lag:
        for lag in lag_dias:
            df_com_lag[f"{feature}_lag_{lag}"] = df_com_lag[feature].shift(lag)

    return df_com_lag.dropna()


def preparar_dataset_com_lag(df):
    """
    Prepara o dataset utilizando lag-features.
    """
    df_lag = criar_lag_features(df)

    features = [
        col
        for col in df_lag.columns
        if "lag" in col
        or col
        in [
            "pressao_atm_media",
            "temp_orvalho_media",
            "umidade_relativa_media",
            "umidade_relativa_minima",
            "umidade_relativa_maxima",
            "vento_vel_media",
        ]
    ]

    X = df_lag[features]
    y = df_lag["temp_maxima"]

    return train_test_split(X, y, test_size=0.2, random_state=42)


# Preparando dados com lag
X_train_com_lag, X_test_com_lag, y_train_com_lag, y_test_com_lag = (
    preparar_dataset_com_lag(df)
)


# %% [markdown]
# ## 3. Avaliação dos Modelos
#  
# ### 3.1 Função de Avaliação

# %% [markdown]
# Definindo Importância das Features

# %%
def avaliar_modelo(modelo, X_train, X_test, y_train, y_test, nome_modelo):
    """
    Treina e avalia um modelo, retornando suas métricas.
    """
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return {"modelo": nome_modelo, "rmse": rmse, "mae": mae, "r2": r2}


# %%
# Definindo modelos sem lag
modelos_sem_lag = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "SVR": SVR(kernel="rbf"),
}
# Treinando e avaliando modelos sem lag
resultados_sem_lag = []
for nome, modelo in modelos_sem_lag.items():
    resultado = avaliar_modelo(
        modelo,
        X_train_sem_lag,
        X_test_sem_lag,
        y_train_sem_lag,
        y_test_sem_lag,
        f"{nome} (Sem Lag)",
    )
    resultados_sem_lag.append(resultado)
    print(f"\nResultados para {nome} (Sem Lag):")
    print(f"RMSE: {resultado['rmse']:.4f}")
    print(f"MAE: {resultado['mae']:.4f}")

# %% [markdown]
# ### 3.2 Treinamento e Avaliação - Sem Lag-Features

# %%
# Definindo modelos sem lag
modelos_sem_lag = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "SVR": SVR(kernel="rbf"),
}

# Treinando e avaliando modelos sem lag
resultados_sem_lag = []
for nome, modelo in modelos_sem_lag.items():
    resultado = avaliar_modelo(
        modelo,
        X_train_sem_lag,
        X_test_sem_lag,
        y_train_sem_lag,
        y_test_sem_lag,
        f"{nome} (Sem Lag)",
    )
    resultados_sem_lag.append(resultado)
    print(f"\nResultados para {nome} (Sem Lag):")
    print(f"RMSE: {resultado['rmse']:.4f}")
    print(f"MAE: {resultado['mae']:.4f}")
    print(f"R²: {resultado['r2']:.4f}")

# %% [markdown]
# ### 3.3 Treinamento e Avaliação - Com Lag-Features

# %%
# Definindo modelos com lag
modelos_com_lag = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "SVR": SVR(kernel="rbf"),
}

# Treinando e avaliando modelos com lag
resultados_com_lag = []
for nome, modelo in modelos_com_lag.items():
    resultado = avaliar_modelo(
        modelo,
        X_train_com_lag,
        X_test_com_lag,
        y_train_com_lag,
        y_test_com_lag,
        f"{nome} (Com Lag)",
    )
    resultados_com_lag.append(resultado)
    print(f"\nResultados para {nome} (Com Lag):")
    print(f"RMSE: {resultado['rmse']:.4f}")
    print(f"MAE: {resultado['mae']:.4f}")
    print(f"R²: {resultado['r2']:.4f}")

# %% [markdown]
# ### Análise de Importância das Features pro Random Forest

# %%
# Random Forest sem Lag
rf_sem_lag = modelos_sem_lag["Random Forest"]
importancias_sem_lag = pd.DataFrame(
    {"Feature": X_train_sem_lag.columns, "Importância": rf_sem_lag.feature_importances_}
).sort_values("Importância", ascending=False)
plt.figure(figsize=(12, 6))
sns.barplot(x="Importância", y="Feature", data=importancias_sem_lag)
plt.title("Importância das Features - Random Forest sem Lag", fontsize=14)
plt.tight_layout()
plt.show()
print("\nImportância das Features - Random Forest sem Lag:")
print(importancias_sem_lag.round(4))

# Random Forest com Lag
rf_com_lag = modelos_com_lag["Random Forest"]
importancias_com_lag = pd.DataFrame(
    {"Feature": X_train_com_lag.columns, "Importância": rf_com_lag.feature_importances_}
).sort_values("Importância", ascending=False)
plt.figure(figsize=(12, 6))
sns.barplot(x="Importância", y="Feature", data=importancias_com_lag)
plt.title("Importância das Features - Random Forest com Lag", fontsize=14)
plt.tight_layout()
plt.show()
print("\nImportância das Features - Random Forest com Lag:")
print(importancias_com_lag.round(4))

# %% [markdown]
# ## 4. Comparação Final e Conclusões

# %%
# Combinando resultados
todos_resultados = pd.DataFrame(resultados_sem_lag + resultados_com_lag)

# Definindo a ordem personalizada dos modelos
ordem_modelos = [
    "Random Forest (Sem Lag)",
    "Random Forest (Com Lag)",
    "Gradient Boosting (Sem Lag)",
    "Gradient Boosting (Com Lag)",
    "SVR (Sem Lag)",
    "SVR (Com Lag)",
]

# Definindo as cores para cada modelo
cores_modelos = {
    "Random Forest (Sem Lag)": "#A1C9F4",  # Azul pastel
    "Random Forest (Com Lag)": "#0072B2",  # Azul mais escuro
    "Gradient Boosting (Sem Lag)": "#B5E384",  # Verde pastel
    "Gradient Boosting (Com Lag)": "#009E73",  # Verde mais escuro
    "SVR (Sem Lag)": "#FFACAC",  # Vermelho pastel
    "SVR (Com Lag)": "#D55E00",  # Vermelho mais escuro
}

# Ordenando o DataFrame
todos_resultados["modelo"] = pd.Categorical(
    todos_resultados["modelo"], categories=ordem_modelos, ordered=True
)
todos_resultados = todos_resultados.sort_values("modelo")

# Criando visualização comparativa do RMSE
plt.figure(figsize=(14, 7))
ax = sns.barplot(
    x="modelo",
    y="rmse",
    data=todos_resultados,
    hue="modelo",
    palette=cores_modelos,
    legend=False,
)
plt.xticks(rotation=45, ha="right")
plt.title("Comparação de RMSE entre Modelos (Com e Sem Lag-Features)", fontsize=14)
plt.xlabel("Modelo", fontsize=12)
plt.ylabel("RMSE", fontsize=12)
plt.tight_layout()

# Adicionando valores nas barras
for i, p in enumerate(ax.patches):
    ax.annotate(
        f"{p.get_height():.4f}",
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="bottom",
        fontsize=10,
        rotation=0,
    )

plt.show()

# Criando visualização comparativa do R²
plt.figure(figsize=(14, 7))
ax = sns.barplot(
    x="modelo",
    y="r2",
    data=todos_resultados,
    hue="modelo",
    palette=cores_modelos,
    legend=False,
)
plt.xticks(rotation=45, ha="right")
plt.title("Comparação de R² entre Modelos (Com e Sem Lag-Features)", fontsize=14)
plt.xlabel("Modelo", fontsize=12)
plt.ylabel("R²", fontsize=12)
plt.tight_layout()

# Adicionando valores nas barras
for i, p in enumerate(ax.patches):
    ax.annotate(
        f"{p.get_height():.4f}",
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="bottom",
        fontsize=10,
        rotation=0,
    )

plt.show()

# Exibindo tabela de resultados
print("\nResultados Detalhados:")
print(todos_resultados.round(4))


# %% [markdown]
# ### Usando as bibliotecas Lime e SHAP pra interpretar melhor e me certificar dos resultados

# %%
import lime
import lime.lime_tabular
import shap
import time

print("Análise de Interpretabilidade dos Modelos ")
# Selecionando o melhor modelo (Random Forest com Lag)
melhor_modelo = modelos_com_lag["Random Forest"]
X_train = X_train_com_lag
X_test = X_test_com_lag
feature_names = X_train.columns.tolist()
# 1. Análise SHAP
print("\nAnálise SHAP")
print("\n\nCalculando valores SHAP...")
# Usando uma amostra para acelerar o cálculo dos valores SHAP
amostra_idx = np.random.choice(
    X_train.shape[0], min(100, X_train.shape[0]), replace=False
)
X_train_amostra = X_train.iloc[amostra_idx]
# Criando o explicador SHAP
explainer = shap.TreeExplainer(melhor_modelo)
shap_values = explainer.shap_values(X_train_amostra)
# Resumo das contribuições das features
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values, X_train_amostra, feature_names=feature_names, show=False)
plt.title("Resumo SHAP - Impacto das Features na Previsão", fontsize=14)
plt.tight_layout()
plt.show()

# %%
# 2. Análise LIME
print("
Análise LIME")
# Criando o explicador LIME
explainer_lime = lime.lime_tabular.LimeTabularExplainer(
X_train.values,
feature_names=feature_names,
class_names=['temp_maxima'],
mode='regression'
)
# Selecionando uma instância aleatória para explicar
idx = np.random.randint(0, len(X_test))
instancia = X_test.iloc[idx]
# Convertendo para DataFrame com os nomes das features para evitar o warning
instancia_df = pd.DataFrame([instancia.values], columns=feature_names)
# Visualizando a explicação LIME
explicacao = explainer_lime.explain_instance(
instancia.values,
lambda x: melhor_modelo.predict(pd.DataFrame(x, columns=feature_names)),
num_features=10
)
# O problema está aqui - a figura vazia é criada antes de chamar␣
↪as_pyplot_figure
# Removendo a criação da figura vazia
# plt.figure(figsize=(10, 6)) # Esta linha cria uma figura vazia

##__________________________________________________________________________________________

# Usando diretamente o método as_pyplot_figure que já cria sua própria figura
fig = explicacao.as_pyplot_figure()
plt.title('LIME - Explicação para uma Previsão Individual', fontsize=14)
plt.tight_layout()
plt.show()
# Comparando previsão vs. valor real
valor_real = y_test_com_lag.iloc[idx]
previsao = melhor_modelo.predict(instancia_df)[0] # Usando DataFrame com nomes␣
↪de colunas
print(f"
Exemplo de Previsão Individual:")
print(f"Valor Real: {valor_real:.2f}")
print(f"Previsão: {previsao:.2f}")
print(f"Diferença: {abs(valor_real - previsao):.2f}")
# 3. Comparação entre as Importâncias das Features (corrigindo numeração)
print("
Comparação entre Métodos de Interpretabilidade")
# Calculando importância média do SHAP
importancia_shap = pd.DataFrame({
'Feature': feature_names,
'SHAP_Importância': np.abs(shap_values).mean(0)
}).sort_values('SHAP_Importância', ascending=False)
# Mesclando as importâncias do Random Forest e SHAP
comparacao_importancias = importancia_shap.merge(
importancias,
on='Feature',
how='inner'
).sort_values('SHAP_Importância', ascending=False).head(10)
# Visualizando a comparação
plt.figure(figsize=(12, 8))
plt.scatter(comparacao_importancias['Importância'],␣
↪comparacao_importancias['SHAP_Importância'])
for i, txt in enumerate(comparacao_importancias['Feature']):
plt.annotate(txt, (comparacao_importancias['Importância'].iloc[i],␣
↪comparacao_importancias['SHAP_Importância'].iloc[i]))
plt.xlabel('Importância Random Forest')
plt.ylabel('Importância SHAP')
plt.title('Correlação entre Importâncias: Random Forest vs SHAP')
plt.grid(True)
plt.tight_layout()
plt.show()
print("
Conclusão da Análise de Interpretabilidade:")
print("1. As features mais importantes segundo o Random Forest são:", ", ".
↪join(importancias.head(3)['Feature'].tolist()))
print("2. As features mais importantes segundo o SHAP são:", ", ".
↪join(importancia_shap.head(3)['Feature'].tolist()))
# Verificando consistência entre os métodos
top5_rf = set(importancias.head(5)['Feature'].tolist())
top5_shap = set(importancia_shap.head(5)['Feature'].tolist())
intersecao = top5_rf.intersection(top5_shap)
print(f"3. Consistência e

# %%
