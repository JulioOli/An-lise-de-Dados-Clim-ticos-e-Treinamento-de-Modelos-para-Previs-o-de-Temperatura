#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Carregar dados originais (sem lag features)
caminho_csv = '/home/iioulos/Documents/IC_Danilo-Cotozika/Dados do INEP que eu solicitei/dados_A707_D_2014-01-01_2025-05-01.csv'

colunas = [
    'data', 'precipitacao_total', 'pressao_atm_media', 
    'temp_orvalho_media', 'temp_maxima', 'temp_media', 
    'temp_minima', 'umidade_relativa_media', 
    'umidade_relativa_minima', 'umidade_relativa_maxima', 
    'vento_vel_media'
]

# Dados sem lag features
df_sem_lags = pd.read_csv(
    caminho_csv,
    sep=',', 
    encoding='latin1',
    skiprows=11,
    header=None,
    names=colunas
)

# Processar dados
df_sem_lags['data'] = pd.to_datetime(df_sem_lags['data'])
df_sem_lags = df_sem_lags.set_index('data')
for col in df_sem_lags.columns:
    df_sem_lags[col] = pd.to_numeric(df_sem_lags[col], errors='coerce')
df_sem_lags = df_sem_lags.interpolate(method='time')
df_sem_lags = df_sem_lags.reset_index()

# Carregar dados com lag features
df_com_lags = pd.read_csv('/home/iioulos/Documents/IC_Danilo-Cotozika/dados_climaticos_com_lags.csv')
df_com_lags['data'] = pd.to_datetime(df_com_lags['data'])

# Features para modelos sem lag
features_sem_lags = ['temp_minima', 'temp_maxima', 'umidade_relativa_media', 'pressao_atm_media']
target = 'temp_media'

# Features para modelos com lag (incluindo as originais + lag features)
features_com_lags = features_sem_lags + [col for col in df_com_lags.columns if '_lag' in col]

# Definir modelos
modelos = {
    'Regressão Linear': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
    'SVR': SVR()
}

# Dicionário para armazenar resultados
resultados = {}

print('=== TREINANDO MODELOS SEM LAG FEATURES ===')
print('-' * 50)

# Preparar dados sem lag
df_sem_lags_clean = df_sem_lags.dropna(subset=features_sem_lags + [target])
X_sem_lags = df_sem_lags_clean[features_sem_lags]
y_sem_lags = df_sem_lags_clean[target]

X_train_sem, X_test_sem, y_train_sem, y_test_sem = train_test_split(
    X_sem_lags, y_sem_lags, test_size=0.2, random_state=42
)

print(f'Dados de treino: {X_train_sem.shape[0]} amostras')
print(f'Dados de teste: {X_test_sem.shape[0]} amostras')
print()

# Treinar modelos sem lag
for nome, modelo in modelos.items():
    print(f'Treinando {nome}...')
    
    # SVR precisa de normalização
    if nome == 'SVR':
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_sem)
        X_test_scaled = scaler.transform(X_test_sem)
        
        modelo.fit(X_train_scaled, y_train_sem)
        y_pred = modelo.predict(X_test_scaled)
    else:
        modelo.fit(X_train_sem, y_train_sem)
        y_pred = modelo.predict(X_test_sem)
    
    rmse = np.sqrt(mean_squared_error(y_test_sem, y_pred))
    r2 = r2_score(y_test_sem, y_pred)
    
    resultados[f'{nome} (Sem Lags)'] = {
        'RMSE': rmse,
        'R2': r2,
        'Tipo': 'Sem Lag Features'
    }
    
    print(f'  RMSE: {rmse:.4f}')
    print(f'  R²: {r2:.4f}')
    print()

print('=== TREINANDO MODELOS COM LAG FEATURES ===')
print('-' * 50)

# Preparar dados com lag
df_com_lags_clean = df_com_lags.dropna(subset=features_com_lags + [target])
X_com_lags = df_com_lags_clean[features_com_lags]
y_com_lags = df_com_lags_clean[target]

X_train_com, X_test_com, y_train_com, y_test_com = train_test_split(
    X_com_lags, y_com_lags, test_size=0.2, random_state=42
)

print(f'Dados de treino: {X_train_com.shape[0]} amostras')
print(f'Dados de teste: {X_test_com.shape[0]} amostras')
print(f'Número de features: {X_train_com.shape[1]}')
print()

# Treinar modelos com lag
for nome, modelo in modelos.items():
    print(f'Treinando {nome} com lag features...')
    
    # SVR precisa de normalização
    if nome == 'SVR':
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_com)
        X_test_scaled = scaler.transform(X_test_com)
        
        modelo.fit(X_train_scaled, y_train_com)
        y_pred = modelo.predict(X_test_scaled)
    else:
        modelo.fit(X_train_com, y_train_com)
        y_pred = modelo.predict(X_test_com)
    
    rmse = np.sqrt(mean_squared_error(y_test_com, y_pred))
    r2 = r2_score(y_test_com, y_pred)
    
    resultados[f'{nome} (Com Lags)'] = {
        'RMSE': rmse,
        'R2': r2,
        'Tipo': 'Com Lag Features'
    }
    
    print(f'  RMSE: {rmse:.4f}')
    print(f'  R²: {r2:.4f}')
    print()

# Criar DataFrame com resultados
df_resultados = pd.DataFrame(resultados).T
df_resultados = df_resultados.reset_index()
df_resultados.columns = ['Modelo', 'RMSE', 'R2', 'Tipo']

print('=== RESULTADOS COMPARATIVOS ===')
print(df_resultados.round(4))

# Salvar resultados
df_resultados.to_csv('/home/iioulos/Documents/IC_Danilo-Cotozika/comparacao_lag_features_completa.csv', index=False)
print('\nResultados salvos em: comparacao_lag_features_completa.csv')

# Calcular melhorias percentuais
melhorias = []
for modelo_base in ['Regressão Linear', 'Random Forest', 'Gradient Boosting', 'SVR']:
    sem_lags = df_resultados[(df_resultados['Modelo'].str.contains(modelo_base)) & (df_resultados['Tipo'] == 'Sem Lag Features')]
    com_lags = df_resultados[(df_resultados['Modelo'].str.contains(modelo_base)) & (df_resultados['Tipo'] == 'Com Lag Features')]
    
    if not sem_lags.empty and not com_lags.empty:
        melhoria_rmse = ((sem_lags['RMSE'].iloc[0] - com_lags['RMSE'].iloc[0]) / sem_lags['RMSE'].iloc[0]) * 100
        melhoria_r2 = ((com_lags['R2'].iloc[0] - sem_lags['R2'].iloc[0]) / sem_lags['R2'].iloc[0]) * 100
        
        melhorias.append({
            'Modelo': modelo_base,
            'Melhoria_RMSE_%': melhoria_rmse,
            'Melhoria_R2_%': melhoria_r2
        })

df_melhorias = pd.DataFrame(melhorias)
print('\n=== MELHORIAS COM LAG FEATURES ===')
print(df_melhorias.round(2))

# Salvar melhorias
df_melhorias.to_csv('/home/iioulos/Documents/IC_Danilo-Cotozika/melhorias_lag_features.csv', index=False)
print('\nMelhorias salvas em: melhorias_lag_features.csv')
