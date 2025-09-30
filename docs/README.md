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

# Dashboard de Análise Climática

Este é um dashboard interativo para visualização e comparação de modelos preditivos com dados climáticos.

## 🚀 Como Visualizar o Dashboard

### Opção 1: Abrir diretamente no navegador (Mais Fácil)
1. Navegue até a pasta do projeto: `/home/iioulos/Documents/IC_Danilo-Cotozika/`
2. Clique duplo no arquivo `dashboard.html`
3. O arquivo será aberto automaticamente no seu navegador padrão

### Opção 2: Arrastar para o navegador
1. Abra seu navegador (Chrome, Firefox, Safari, etc.)
2. Arraste o arquivo `dashboard.html` para dentro da janela do navegador

### Opção 3: Usar Live Server no VS Code (Recomendado para desenvolvimento)
1. Abra o VS Code
2. Instale a extensão "Live Server" (se ainda não tiver)
3. Clique com o botão direito no arquivo `dashboard.html`
4. Selecione "Open with Live Server"

## 📊 Funcionalidades do Dashboard

### 🏆 Comparação de Modelos
- **Visualização de Performance**: Tabela com todos os modelos e suas métricas
- **Filtros Interativos**: Marque/desmarque RMSE e R² para customizar a visualização
- **Ranking Automático**: O melhor modelo é destacado automaticamente
- **Insights Dinâmicos**: Análise automática do melhor modelo

### 📈 Dados Climáticos
- **Tabela Paginada**: Navegue pelos dados com controles de paginação
- **Controle de Itens**: Escolha quantos registros ver por página (5, 10, 20)
- **Dados Completos**: Todas as variáveis climáticas importantes
- **Interface Responsiva**: Funciona em desktop, tablet e mobile

### 🎨 Interface
- **Design Moderno**: Interface limpa com Tailwind CSS
- **Animações Suaves**: Transições e efeitos visuais
- **Cores Intuitivas**: Sistema de cores para fácil identificação
- **Emojis e Ícones**: Visual amigável e profissional

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estrutura da página
- **CSS3**: Estilização (via Tailwind CSS CDN)
- **JavaScript**: Funcionalidades interativas
- **Tailwind CSS**: Framework de CSS utilitário

## 📋 Dados Incluídos

### Modelos de Machine Learning
- Linear Regression
- Linear Regression (com Lags)
- Random Forest Regressor
- Gradient Boosting Regressor
- Support Vector Regressor

### Variáveis Climáticas
- Data
- Precipitação (mm)
- Pressão Atmosférica (hPa)
- Temperatura Média (°C)
- Temperatura Máxima (°C)
- Temperatura Mínima (°C)
- Umidade Relativa (%)
- Velocidade do Vento (km/h)
- Radiação Solar
- Evapotranspiração

## 🔧 Personalização

Para modificar os dados ou aparência:

1. **Dados dos Modelos**: Edite o array `modelData` no JavaScript
2. **Dados Climáticos**: Modifique a string `rawClimateText`
3. **Cores e Estilo**: Altere as classes Tailwind CSS
4. **Funcionalidades**: Adicione novo JavaScript conforme necessário

## 📱 Compatibilidade

✅ Chrome 80+
✅ Firefox 75+
✅ Safari 13+
✅ Edge 80+
✅ Mobile browsers

## 📞 Suporte

Se encontrar algum problema:
1. Verifique se está usando um navegador moderno
2. Certifique-se de que o JavaScript está habilitado
3. Teste em outro navegador se necessário

---

**Desenvolvido para análise de modelos climáticos** 🌤️