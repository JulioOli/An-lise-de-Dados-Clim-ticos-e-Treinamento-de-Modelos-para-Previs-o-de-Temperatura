# Análise de Dados Climáticos e Treinamento de Modelos para Previsão de Temperatura

Este repositório contém um projeto de análise de dados climáticos e desenvolvimento de modelos preditivos para previsão de temperatura.

## Conteúdo

- **Análise Exploratória de Dados**: Notebooks com análise detalhada dos dados climáticos históricos
- **Modelos de Machine Learning**: Implementação e comparação de diferentes modelos para previsão de temperatura
- **Visualizações**: Gráficos e visualizações dos dados e resultados dos modelos
- **Modelos Salvos**: Arquivos .joblib com os modelos treinados

## Principais Arquivos

- `Analise_Comparativa_Modelos.ipynb`: Notebook com comparação detalhada entre diferentes modelos
- `EDA_e_Treinamento_de_Modelos_dados-INMET.ipynb`: Notebook com análise exploratória e treinamento inicial
- `dados_climaticos_com_lags.csv`: Dataset processado com features de lag para treinamento
- `model_comparison_results.csv`: Resultados comparativos dos diferentes modelos

## Requisitos

Os requisitos do projeto estão listados no arquivo `requirements.txt`.

```
pip install -r requirements.txt
```

## Modelos Implementados

- Regressão Linear
- Random Forest
- Gradient Boosting
- Support Vector Regression (SVR)

## Resultados

Os modelos foram avaliados utilizando métricas como RMSE, MAE e R². Os resultados detalhados podem ser encontrados nos notebooks de análise. 