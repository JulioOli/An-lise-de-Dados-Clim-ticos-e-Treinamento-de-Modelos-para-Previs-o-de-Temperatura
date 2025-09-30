# 🌤️ Análise Comparativa de Modelos Climáticos

## Descrição
Este projeto apresenta uma análise comparativa sistemática de modelos de machine learning para previsão de dados meteorológicos, comparando abordagens com e sem lag-features.


## 🎯 Principais Descobertas

- ✅ **Random Forest sem lag features** foi o melhor modelo (R² = 0.9121)
- ⚠️ **Lag features não melhoraram** a performance paradoxalmente
- 🔥 **temp_maxima_lag_1** é a feature mais importante quando presente (58.9%)
- 📊 **Pressão atmosférica** e **umidade relativa mínima** são cruciais sem lag features

## 🚀 Como Executar

### Dashboard Web (React)
```bash
cd website/
npm install
npm start
# Acesse: http://localhost:3000
```

### Dashboard Streamlit
```bash
pip install -r requirements.txt
cd dashboards/
streamlit run dashboard_streamlit.py
```

### Notebooks
```bash
pip install -r requirements.txt
jupyter lab notebooks/
```

## 🛠️ Tecnologias Utilizadas

- **Python**: Pandas, Scikit-learn, Matplotlib, Seaborn
- **Machine Learning**: Random Forest, Gradient Boosting, SVR
- **Interpretabilidade**: SHAP, LIME
- **Web**: React, Vite, Tailwind CSS, Recharts
- **Dashboards**: Streamlit, Plotly

## 📊 Modelos Avaliados

| Modelo | Tipo | RMSE | R² | MAE |
|--------|------|------|----|----|
| Random Forest | Sem Lag | 1.1567 | **0.9121** | 0.8492 |
| Gradient Boosting | Sem Lag | 1.2518 | 0.8970 | 0.9228 |
| Random Forest | Com Lag | 1.2936 | 0.8786 | 0.9328 |
| Gradient Boosting | Com Lag | 1.2680 | 0.8834 | 0.9474 |
| SVR | Sem Lag | 3.5487 | 0.1724 | 2.7225 |
| SVR | Com Lag | 3.5256 | 0.0983 | 2.7268 |

## 🔬 Metodologia

1. **Preparação dos Dados**: Carregamento dos dados INMET, tratamento de valores faltantes
2. **Feature Engineering**: Criação de lag features (1, 2, 3, 7 dias)
3. **Modelagem**: Treinamento de 6 modelos diferentes
4. **Avaliação**: Métricas RMSE, MAE, R²
5. **Interpretabilidade**: Análise SHAP e LIME

## 📈 Visualizações

O projeto inclui dashboards interativos com:
- Comparações de performance entre modelos
- Análises de correlação
- Importância das features
- Análises de interpretabilidade
- Dados técnicos e metodologia

## 🤝 Contribuição

Este é um projeto de Iniciação Científica desenvolvido por Danilo Cotozika.

## 📧 Contato

Para mais informações sobre o projeto, entre em contato através do repositório.
