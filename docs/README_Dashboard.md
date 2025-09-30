# 🌤️ Dashboard de Análise Climática INMET

Dashboard interativo para análise de dados climáticos do INMET (Instituto Nacional de Meteorologia) com integração de modelos de Machine Learning para previsão de temperatura.

## 📋 Funcionalidades

### 📊 Visão Geral
- **Métricas principais**: Melhor R² dos modelos, total de registros, temperatura e umidade médias
- **Distribuições visuais**: Dados por estação do ano e frequência de precipitação
- **Estatísticas resumo**: Análise descritiva das principais variáveis

### 🤖 Modelos de Machine Learning
- **Comparação de performance**: RMSE e R² de diferentes modelos
- **Ranking de modelos**: Tabela ordenada por performance
- **Impacto das Lag Features**: Análise de melhorias com features temporais
- **Modelos incluídos**:
  - Linear Regression
  - Random Forest Regressor
  - Gradient Boosting Regressor
  - Support Vector Regressor (SVR)

### 📈 Séries Temporais
- **Visualização interativa** de múltiplas variáveis climáticas
- **Filtros de período**: Seleção de data inicial e final
- **Análise sazonal**: Padrões mensais de temperatura
- **Variáveis disponíveis**:
  - Temperatura média, máxima e mínima
  - Umidade relativa
  - Pressão atmosférica
  - Precipitação total

### 🔗 Análise de Correlação
- **Mapa de calor** das correlações entre variáveis
- **Ranking das correlações** mais fortes
- **Correlação com Lag Features** (quando disponível)

### 📊 Distribuições e Histogramas
- **Histogramas** de temperatura e umidade
- **Box plots** por estação do ano
- **Densidade de precipitação** em dias chuvosos

### 📉 Scatter Plots
- **Relações bivariadas** entre variáveis climáticas
- **Linhas de tendência** para identificar padrões
- **Coloração por estação** do ano

### 📋 Dados Brutos
- **Tabela interativa** com todos os dados
- **Filtros por período** e estação
- **Download em CSV** dos dados filtrados
- **Estatísticas do período** selecionado

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.7 ou superior
- Dados do INMET no formato CSV

### Instalação Rápida

1. **Clone ou baixe o projeto**
```bash
cd /caminho/para/o/projeto
```

2. **Execute o script de configuração**
```bash
./setup_dashboard.sh
```

### Instalação Manual

1. **Criar ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. **Instalar dependências**
```bash
pip install streamlit plotly pandas numpy scikit-learn seaborn matplotlib joblib
```

3. **Executar o dashboard**
```bash
streamlit run dashboard_streamlit.py
```

## 📁 Estrutura dos Dados

### Dados Principais (INMET)
- **Fonte**: `/Dados do INEP que eu solicitei/dados_A707_D_2014-01-01_2025-05-01.csv`
- **Estação**: PRESIDENTE PRUDENTE (A707)
- **Período**: 2014-2025
- **Coordenadas**: Latitude -22.12°, Longitude -51.41°, Altitude 431.92m

### Variáveis Incluídas
- `data`: Data da medição
- `precipitacao_total`: Precipitação total diária (mm)
- `pressao_atm_media`: Pressão atmosférica média (mB)
- `temp_orvalho_media`: Temperatura do ponto de orvalho (°C)
- `temp_maxima`: Temperatura máxima diária (°C)
- `temp_media`: Temperatura média diária (°C)
- `temp_minima`: Temperatura mínima diária (°C)
- `umidade_relativa_media`: Umidade relativa média (%)
- `umidade_relativa_minima`: Umidade relativa mínima (%)
- `umidade_relativa_maxima`: Umidade relativa máxima (%)
- `vento_vel_media`: Velocidade média do vento (m/s)

### Dados Derivados
- **Estações do ano**: Classificação automática baseada no mês
- **Categorias de precipitação**: Nenhuma, Leve, Moderada, Pesada
- **Lag Features**: Variáveis temporais defasadas (quando disponível)

## 📊 Resultados dos Modelos

### Performance dos Modelos (com Lag Features)
| Modelo | RMSE | R² |
|--------|------|-----|
| **Gradient Boosting** | **0.568** | **0.971** |
| Random Forest | 0.570 | 0.971 |
| Linear Regression | 0.658 | 0.964 |
| Support Vector Regressor | 0.599 | 0.967 |

### Melhorias com Lag Features
- **Random Forest**: 24% melhoria no RMSE
- **Gradient Boosting**: 27.2% melhoria no RMSE  
- **SVR**: 26.9% melhoria no RMSE
- **Linear Regression**: 0.3% melhoria no RMSE

## 🚀 Como Usar

1. **Acesse o dashboard** em `http://localhost:8501`
2. **Navegue pelas abas** usando a barra lateral
3. **Explore as visualizações** interativas
4. **Ajuste os filtros** conforme necessário
5. **Baixe os dados** filtrados quando necessário

## 🎨 Características Técnicas

- **Framework**: Streamlit para interface web
- **Visualizações**: Plotly para gráficos interativos
- **Processamento**: Pandas e NumPy
- **Machine Learning**: Scikit-learn
- **Cache inteligente**: Carregamento otimizado dos dados
- **Responsivo**: Interface adaptável

## 📧 Suporte

Para questões técnicas ou sugestões:
- Verifique se todos os arquivos CSV estão nos caminhos corretos
- Confirme que o ambiente virtual está ativado
- Verifique se todas as dependências foram instaladas

## 📄 Licença

Este projeto foi desenvolvido para análise acadêmica e científica dos dados climáticos do INMET.

---

**Desenvolvido com ❤️ para análise climática** 🌤️
