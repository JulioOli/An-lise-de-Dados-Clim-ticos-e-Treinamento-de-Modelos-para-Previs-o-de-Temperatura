# 🌤️ Dashboard de Análise Climática - Guia de Execução

## 🚀 Como Executar o Dashboard

Você já tem um ambiente virtual configurado! Para executar o dashboard:

### Opção 1: Script Automático (Recomendado)
```bash
./executar_dashboard.sh
```

### Opção 2: Comando Manual
```bash
./venv/bin/streamlit run dashboard_streamlit.py
```

### Opção 3: Ativando o Ambiente Virtual
```bash
source venv/bin/activate
streamlit run dashboard_streamlit.py
```

## 📍 Acessar o Dashboard

Após executar, acesse: **http://localhost:8501**

## 🎨 Interface e Navegação

### **Navegação Visual**
- ✅ **Botões sempre visíveis** no topo da página
- ✅ **Indicador visual** da página atual
- ✅ **7 seções organizadas** em duas fileiras de botões
- ✅ **Design responsivo** e intuitivo

### **Botões de Navegação**
**Fileira Superior:**
- 📊 Visão Geral | 🤖 Modelos ML | 📈 Séries Temporais | 🔗 Correlação

**Fileira Inferior:**
- 📊 Distribuições | 📉 Scatter Plots | 📋 Dados

### **Funcionalidades Visuais**
- **Botão ativo**: Destacado em azul com sombra
- **Hover effect**: Animação ao passar o mouse
- **Indicador de página**: Banner colorido mostrando seção atual
- **Métricas principais**: Melhor R² dos modelos, registros analisados, temperatura e umidade médias
- **Gráficos de pizza**: Distribuição por estação e frequência de precipitação
- **Estatísticas resumo**: Análise descritiva das variáveis

### 🤖 Modelos ML
- **Comparação de performance**: RMSE e R² de diferentes modelos
- **Ranking de modelos**: Tabela ordenada por performance
- **Impacto das Lag Features**: Melhorias com features temporais
- **Modelos incluídos**: Linear Regression, Random Forest, Gradient Boosting, SVR

### 📈 Séries Temporais
- **Visualização interativa** de múltiplas variáveis
- **Filtros de período** personalizáveis
- **Análise sazonal** mensal

### 🔗 Correlação
- **Mapa de calor** das correlações
- **Ranking das correlações** mais fortes
- **Correlação com Lag Features**

### 📊 Distribuições
- **Histogramas** de temperatura e umidade
- **Box plots** por estação
- **Densidade de precipitação**

### 📉 Scatter Plots
- **Relações bivariadas** entre variáveis
- **Linhas de tendência**
- **Coloração por estação**

### 📋 Dados Brutos
- **Tabela interativa** filtável
- **Download em CSV**
- **Estatísticas do período selecionado**

## 📁 Estrutura dos Dados

### Dados Principais
- **Estação**: PRESIDENTE PRUDENTE (A707)
- **Período**: 2014-2025
- **Localização**: -22.12°, -51.41°, 431.92m altitude

### Variáveis Analisadas
- Temperatura (média, máxima, mínima)
- Umidade relativa
- Pressão atmosférica
- Precipitação total
- Velocidade do vento
- Temperatura do ponto de orvalho

### Resultados dos Modelos
| Modelo | RMSE | R² |
|--------|------|-----|
| **Gradient Boosting** | **0.568** | **0.971** |
| Random Forest | 0.570 | 0.971 |
| Linear Regression | 0.658 | 0.964 |
| SVR | 0.599 | 0.967 |

## 🛠️ Dependências

As seguintes bibliotecas são necessárias (já instaladas no seu ambiente):
- streamlit
- plotly
- pandas
- numpy
- scikit-learn
- seaborn
- matplotlib
- statsmodels (para linhas de tendência nos scatter plots)

## 📧 Troubleshooting

### Dashboard não inicia?
1. Verifique se está no diretório correto
2. Confirme que o ambiente virtual existe: `ls venv/`
3. Execute: `./venv/bin/pip install streamlit plotly`

### Dados não carregam?
1. Verifique se os CSVs estão nos caminhos corretos
2. Confirme a estrutura dos arquivos de dados

### Porta já em uso?
```bash
./venv/bin/streamlit run dashboard_streamlit.py --server.port 8502
```

---

**Dashboard desenvolvido com ❤️ para análise climática do INMET** 🌤️
