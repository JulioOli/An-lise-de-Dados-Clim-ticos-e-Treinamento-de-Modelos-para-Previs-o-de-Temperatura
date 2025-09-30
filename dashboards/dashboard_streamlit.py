"""
Dashboard Climático Simplificado e Otimizado
Baseado nos dados do INMET e análises realizadas
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import warnings
import os
import joblib
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard Climático",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para estilização - SEM DESTAQUE AZUL
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .metric-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px;
        text-align: center;
    }
    
    /* Estilizar botões de navegação - TODOS IGUAIS */
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #ddd;
        margin: 2px;
        transition: all 0.3s ease;
        background-color: #f8f9fa !important;
        border-color: #dee2e6 !important;
        color: #495057 !important;
    }
    
    /* Hover effect */
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Indicador de página atual */
    .current-page {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Cores personalizadas
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8'
}

# Cache para carregar dados
@st.cache_data
def load_data():
    """Carrega todos os datasets necessários"""
    try:
        # Carregar dados principais
        dados_lag = pd.read_csv('dados_climaticos_com_lags.csv')
        dados_lag['data'] = pd.to_datetime(dados_lag['data'])
        
        # Comparação de modelos
        comparison_df = pd.read_csv('model_comparison_results.csv')
        
        # Melhorias com lag features
        melhorias_df = pd.read_csv('melhorias_lag_features.csv')
        
        # Comparação completa lag features
        comparacao_completa = pd.read_csv('comparacao_lag_features_completa.csv')
        
        return dados_lag, comparison_df, melhorias_df, comparacao_completa
    
    except FileNotFoundError as e:
        st.error(f"Arquivo não encontrado: {e}")
        return None, None, None, None

# Função para criar gráfico de tendência
def create_trend_plot(data, x_col, y_col, title):
    """Cria gráfico de linha com tendência"""
    fig = px.line(data, x=x_col, y=y_col, title=title,
                  color_discrete_sequence=[COLORS['primary']])
    
    # Adicionar linha de tendência
    z = np.polyfit(range(len(data)), data[y_col].dropna(), 1)
    p = np.poly1d(z)
    fig.add_scatter(x=data[x_col], y=p(range(len(data))), 
                   mode='lines', name='Tendência', 
                   line=dict(dash='dash', color=COLORS['secondary']))
    
    fig.update_layout(
        xaxis_title=x_col.title(),
        yaxis_title=y_col.title(),
        template='plotly_white',
        height=400
    )
    return fig

# Função para criar matriz de correlação
def create_correlation_matrix(data, columns):
    """Cria matriz de correlação interativa"""
    corr_matrix = data[columns].corr()
    
    fig = px.imshow(corr_matrix, 
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    title="Matriz de Correlação",
                    labels=dict(color="Correlação"))
    
    fig.update_layout(height=500)
    return fig

# Header principal
st.markdown('<h1 class="main-header">🌤️ Dashboard Climático INMET</h1>', unsafe_allow_html=True)

# Navegação com botões horizontais
st.markdown("### 📋 Navegação")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    btn_overview = st.button("📊 Visão Geral", width="stretch")
with col2:
    btn_models = st.button("🤖 Modelos ML", width="stretch")
with col3:
    btn_timeseries = st.button("📈 Séries Temporais", width="stretch")
with col4:
    btn_correlation = st.button("🔗 Correlação", width="stretch")
with col5:
    btn_distributions = st.button("📊 Distribuições", width="stretch")
with col6:
    btn_scatter = st.button("📉 Scatter Plots", width="stretch")
with col7:
    btn_data = st.button("📋 Dados", width="stretch")

# Carregar dados
dados_lag, comparison_df, melhorias_df, comparacao_completa = load_data()

if dados_lag is None:
    st.error("❌ Erro ao carregar os dados. Verifique se os arquivos CSV estão no diretório.")
    st.stop()

# Inicializar sessão
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'overview'

# Atualizar página baseado nos botões clicados
if btn_overview:
    st.session_state.current_page = 'overview'
elif btn_models:
    st.session_state.current_page = 'models'
elif btn_timeseries:
    st.session_state.current_page = 'timeseries'
elif btn_correlation:
    st.session_state.current_page = 'correlation'
elif btn_distributions:
    st.session_state.current_page = 'distributions'
elif btn_scatter:
    st.session_state.current_page = 'scatter'
elif btn_data:
    st.session_state.current_page = 'data'

# ==================== SEÇÃO: VISÃO GERAL ====================
if st.session_state.current_page == 'overview':
    st.markdown('<div class="current-page">📊 Visão Geral dos Dados</div>', unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Total de Registros", f"{len(dados_lag):,}")
    
    with col2:
        temp_media = dados_lag['temp_media'].mean()
        st.metric("🌡️ Temperatura Média", f"{temp_media:.1f}°C")
    
    with col3:
        precip_total = dados_lag['precipitacao_total'].sum()
        st.metric("🌧️ Precipitação Total", f"{precip_total:.0f}mm")
    
    with col4:
        umidade_media = dados_lag['umidade_relativa_media'].mean()
        st.metric("💧 Umidade Média", f"{umidade_media:.1f}%")
    
    st.markdown("---")
    
    # Gráficos de overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperatura ao longo do tempo
        fig_temp = create_trend_plot(dados_lag.tail(365), 'data', 'temp_media', 
                                   '🌡️ Temperatura Média (Último Ano)')
        st.plotly_chart(fig_temp, width='stretch')
    
    with col2:
        # Precipitação ao longo do tempo
        fig_precip = create_trend_plot(dados_lag.tail(365), 'data', 'precipitacao_total', 
                                     '🌧️ Precipitação (Último Ano)')
        st.plotly_chart(fig_precip, width='stretch')

# ==================== SEÇÃO: MODELOS ML ====================
elif st.session_state.current_page == 'models':
    st.markdown('<div class="current-page">🤖 Comparação de Modelos de Machine Learning</div>', unsafe_allow_html=True)
    
    if comparacao_completa is not None:
        # Tabela de comparação
        st.subheader("📊 Performance dos Modelos")
        st.dataframe(comparacao_completa, width='stretch')
        
        # Cores específicas para cada categoria - tons de azul
        cores_categoria = {
            'Com Lag Features': '#1f77b4',  # Azul escuro para com lag
            'Sem Lag Features': '#aec7e8'   # Azul claro para sem lag
        }
        
        # Gráfico principal: R² Score com destaque para lag features
        fig_r2 = go.Figure()
        
        for categoria in comparacao_completa['Tipo'].unique():
            df_cat = comparacao_completa[comparacao_completa['Tipo'] == categoria]
            fig_r2.add_trace(go.Bar(
                name=categoria,
                x=df_cat['Modelo'],
                y=df_cat['R2'],
                marker_color=cores_categoria[categoria],
                text=[f'{r2:.3f}' for r2 in df_cat['R2']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>R² Score: %{y:.3f}<extra></extra>'
            ))
        
        fig_r2.update_layout(
            title='📊 Comparação R² Score: Modelos com vs sem Lag Features',
            xaxis_title='Modelos',
            yaxis_title='R² Score',
            height=500,
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_r2, width='stretch')
        
        # Gráfico de RMSE com destaque para lag features
        fig_rmse = go.Figure()
        
        for categoria in comparacao_completa['Tipo'].unique():
            df_cat = comparacao_completa[comparacao_completa['Tipo'] == categoria]
            fig_rmse.add_trace(go.Bar(
                name=categoria,
                x=df_cat['Modelo'],
                y=df_cat['RMSE'],
                marker_color=cores_categoria[categoria],
                text=[f'{rmse:.3f}' for rmse in df_cat['RMSE']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>RMSE: %{y:.3f}<extra></extra>'
            ))
        
        fig_rmse.update_layout(
            title='📉 Comparação RMSE: Modelos com vs sem Lag Features',
            xaxis_title='Modelos',
            yaxis_title='RMSE',
            height=500,
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_rmse, width='stretch')
        
        # Análise comparativa
        st.subheader("🔍 Análise Comparativa")
        
        # Calcular melhorias
        sem_lag = comparacao_completa[comparacao_completa['Tipo'] == 'Sem Lag Features']
        com_lag = comparacao_completa[comparacao_completa['Tipo'] == 'Com Lag Features']
        
        if len(sem_lag) > 0 and len(com_lag) > 0:
            melhor_r2_sem = sem_lag['R2'].max()
            melhor_r2_com = com_lag['R2'].max()
            melhor_rmse_sem = sem_lag['RMSE'].min()
            melhor_rmse_com = com_lag['RMSE'].min()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Melhor R² (Sem Lag)", f"{melhor_r2_sem:.3f}")
            with col2:
                st.metric("Melhor R² (Com Lag)", f"{melhor_r2_com:.3f}")
            with col3:
                st.metric("Melhor RMSE (Sem Lag)", f"{melhor_rmse_sem:.3f}")
            with col4:
                st.metric("Melhor RMSE (Com Lag)", f"{melhor_rmse_com:.3f}")
            
            # Calcular melhorias percentuais
            melhoria_r2 = ((melhor_r2_com - melhor_r2_sem) / melhor_r2_sem) * 100
            melhoria_rmse = ((melhor_rmse_sem - melhor_rmse_com) / melhor_rmse_sem) * 100
            
            st.success(f"🎯 **Melhoria com Lag Features:** R² +{melhoria_r2:.1f}% | RMSE -{melhoria_rmse:.1f}%")
        
        # Tabela de ranking
        st.subheader("🏆 Ranking de Performance")
        ranking_df = comparacao_completa.sort_values('R2', ascending=False).reset_index(drop=True)
        ranking_df['Posição'] = range(1, len(ranking_df) + 1)
        ranking_df = ranking_df[['Posição', 'Modelo', 'Tipo', 'R2', 'RMSE']]
        
        # Aplicar cores na tabela - tons de azul com melhor contraste
        def highlight_lag_features(row):
            if row['Tipo'] == 'Com Lag Features':
                return ['background-color: #1976D2; color: white'] * len(row)  # Azul escuro com texto branco
            else:
                return ['background-color: #42A5F5; color: white'] * len(row)  # Azul médio com texto branco
        
        st.dataframe(
            ranking_df.style.apply(highlight_lag_features, axis=1),
            width='stretch'
        )
    else:
        st.error("❌ Erro ao carregar dados de comparação. Verifique se o arquivo 'comparacao_lag_features_completa.csv' existe.")

# ==================== SEÇÃO: SÉRIES TEMPORAIS ====================
elif st.session_state.current_page == 'timeseries':
    st.markdown('<div class="current-page">📈 Análise de Séries Temporais</div>', unsafe_allow_html=True)
    
    # Seletor de variável
    variavel = st.selectbox("Selecione a variável para análise:",
                           ['temp_media', 'precipitacao_total', 'umidade_relativa_media', 'pressao_atm_media'])
    
    # Período de análise
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data de início:", dados_lag['data'].min())
    with col2:
        data_fim = st.date_input("Data de fim:", dados_lag['data'].max())
    
    # Filtrar dados
    mask = (dados_lag['data'] >= pd.to_datetime(data_inicio)) & (dados_lag['data'] <= pd.to_datetime(data_fim))
    dados_filtrados = dados_lag.loc[mask]
    
    # Gráfico principal
    fig_ts = create_trend_plot(dados_filtrados, 'data', variavel, 
                              f'Série Temporal: {variavel.replace("_", " ").title()}')
    st.plotly_chart(fig_ts, width="stretch")
    
    # Análise sazonal
    st.subheader("📅 Análise Sazonal")
    dados_filtrados['mes'] = dados_filtrados['data'].dt.month
    dados_mensais = dados_filtrados.groupby('mes')[variavel].mean().reset_index()
    
    fig_sazonal = px.line(dados_mensais, x='mes', y=variavel,
                         title=f'Padrão Sazonal - {variavel.replace("_", " ").title()}',
                         markers=True)
    fig_sazonal.update_xaxes(tickmode='array', tickvals=list(range(1, 13)),
                            ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    st.plotly_chart(fig_sazonal, width="stretch")

# ==================== SEÇÃO: CORRELAÇÃO ====================
elif st.session_state.current_page == 'correlation':
    st.markdown('<div class="current-page">🔗 Análise de Correlação</div>', unsafe_allow_html=True)
    
    # Variáveis numéricas
    numeric_cols = ['temp_media', 'precipitacao_total', 'umidade_relativa_media', 'pressao_atm_media']
    
    # Matriz de correlação
    fig_corr = create_correlation_matrix(dados_lag, numeric_cols)
    st.plotly_chart(fig_corr, width="stretch")
    
    # Correlações mais fortes
    st.subheader("🔍 Correlações Mais Significativas")
    corr_matrix = dados_lag[numeric_cols].corr()
    
    # Extrair correlações (excluindo diagonal)
    correlacoes = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            var1 = corr_matrix.columns[i]
            var2 = corr_matrix.columns[j]
            corr_val = corr_matrix.iloc[i, j]
            correlacoes.append({
                'Variável 1': var1,
                'Variável 2': var2,
                'Correlação': corr_val
            })
    
    df_correlacoes = pd.DataFrame(correlacoes)
    df_correlacoes = df_correlacoes.reindex(df_correlacoes['Correlação'].abs().sort_values(ascending=False).index)
    
    st.dataframe(df_correlacoes, width="stretch")

# ==================== SEÇÃO: DISTRIBUIÇÕES ====================
elif st.session_state.current_page == 'distributions':
    st.markdown('<div class="current-page">📊 Análise de Distribuições</div>', unsafe_allow_html=True)
    
    # Histogramas
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_temp = px.histogram(dados_lag, x='temp_media', nbins=50,
                                   title='Distribuição da Temperatura Média',
                                   color_discrete_sequence=[COLORS['primary']])
        st.plotly_chart(fig_hist_temp, width="stretch")
        
        fig_hist_umid = px.histogram(dados_lag, x='umidade_relativa_media', nbins=50,
                                   title='Distribuição da Umidade Relativa',
                                   color_discrete_sequence=[COLORS['info']])
        st.plotly_chart(fig_hist_umid, width="stretch")
    
    with col2:
        fig_hist_precip = px.histogram(dados_lag, x='precipitacao_total', nbins=50,
                                     title='Distribuição da Precipitação',
                                     color_discrete_sequence=[COLORS['secondary']])
        st.plotly_chart(fig_hist_precip, width="stretch")
        
        fig_hist_press = px.histogram(dados_lag, x='pressao_atm_media', nbins=50,
                                    title='Distribuição da Pressão Atmosférica',
                                    color_discrete_sequence=[COLORS['success']])
        st.plotly_chart(fig_hist_press, width="stretch")
    
    # Box plots
    st.subheader("📦 Box Plots - Detecção de Outliers")
    
    # Criar subplots
    from plotly.subplots import make_subplots
    fig_box = make_subplots(rows=2, cols=2, 
                           subplot_titles=['Temperatura', 'Precipitação', 'Umidade', 'Pressão'])
    
    # Adicionar box plots
    fig_box.add_box(y=dados_lag['temp_media'], name='Temperatura', row=1, col=1)
    fig_box.add_box(y=dados_lag['precipitacao_total'], name='Precipitação', row=1, col=2)
    fig_box.add_box(y=dados_lag['umidade_relativa_media'], name='Umidade', row=2, col=1)
    fig_box.add_box(y=dados_lag['pressao_atm_media'], name='Pressão', row=2, col=2)
    
    fig_box.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_box, width="stretch")

# ==================== SEÇÃO: SCATTER PLOTS ====================
elif st.session_state.current_page == 'scatter':
    st.markdown('<div class="current-page">📉 Scatter Plots e Relações</div>', unsafe_allow_html=True)
    
    # Seletores para variáveis
    col1, col2 = st.columns(2)
    
    with col1:
        var_x = st.selectbox("Variável X:", 
                           ['temp_media', 'precipitacao_total', 'umidade_relativa_media', 'pressao_atm_media'],
                           index=0)
    
    with col2:
        var_y = st.selectbox("Variável Y:", 
                           ['temp_media', 'precipitacao_total', 'umidade_relativa_media', 'pressao_atm_media'],
                           index=1)
    
    # Scatter plot principal
    fig_scatter = px.scatter(dados_lag, x=var_x, y=var_y,
                           title=f'Relação entre {var_x.replace("_", " ").title()} e {var_y.replace("_", " ").title()}',
                           color_discrete_sequence=[COLORS['primary']],
                           opacity=0.6)
    
    # Adicionar linha de tendência usando statsmodels
    try:
        import statsmodels.api as sm
        
        # Remover valores NaN
        data_clean = dados_lag[[var_x, var_y]].dropna()
        
        if len(data_clean) > 0:
            X = sm.add_constant(data_clean[var_x])
            model = sm.OLS(data_clean[var_y], X).fit()
            
            # Criar linha de predição
            x_range = np.linspace(data_clean[var_x].min(), data_clean[var_x].max(), 100)
            X_pred = sm.add_constant(x_range)
            y_pred = model.predict(X_pred)
            
            fig_scatter.add_scatter(x=x_range, y=y_pred, mode='lines', 
                                  name='Linha de Tendência',
                                  line=dict(color=COLORS['secondary'], width=3))
    except ImportError:
        st.warning("Statsmodels não instalado. Linha de tendência não disponível.")
    
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, width="stretch")
    
    # Scatter plots matriz
    st.subheader("🎯 Matriz de Scatter Plots")
    numeric_cols = ['temp_media', 'precipitacao_total', 'umidade_relativa_media', 'pressao_atm_media']
    
    # Criar scatter matrix
    fig_matrix = px.scatter_matrix(dados_lag[numeric_cols].sample(1000), 
                                 dimensions=numeric_cols,
                                 title="Matriz de Scatter Plots (Amostra de 1000 pontos)")
    fig_matrix.update_layout(height=800)
    st.plotly_chart(fig_matrix, width="stretch")

# ==================== SEÇÃO: DADOS BRUTOS ====================
elif st.session_state.current_page == 'data':
    st.markdown('<div class="current-page">📋 Dados Brutos e Informações</div>', unsafe_allow_html=True)
    
    # Informações dos datasets
    st.subheader("ℹ️ Informações dos Datasets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📊 Dados Principais", f"{len(dados_lag)} registros")
        st.metric("📅 Período", f"{dados_lag['data'].min().strftime('%d/%m/%Y')} - {dados_lag['data'].max().strftime('%d/%m/%Y')}")
    
    with col2:
        if comparison_df is not None:
            st.metric("🤖 Modelos Avaliados", len(comparison_df))
        if melhorias_df is not None:
            st.metric("📈 Melhorias Registradas", len(melhorias_df))
    
    # Prévia dos dados
    st.subheader("👁️ Prévia dos Dados Principais")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        n_registros = st.slider("Número de registros:", 10, 1000, 100)
    
    with col2:
        tipo_amostra = st.selectbox("Tipo de amostra:", ["Últimos registros", "Primeiros registros", "Aleatório"])
    
    with col3:
        colunas_selecionadas = st.multiselect("Colunas:", 
                                            dados_lag.columns.tolist(),
                                            default=['data', 'temp_media', 'precipitacao_total', 'umidade_relativa_media'])
    
    # Mostrar dados filtrados
    if tipo_amostra == "Últimos registros":
        dados_mostrar = dados_lag[colunas_selecionadas].tail(n_registros)
    elif tipo_amostra == "Primeiros registros":
        dados_mostrar = dados_lag[colunas_selecionadas].head(n_registros)
    else:
        dados_mostrar = dados_lag[colunas_selecionadas].sample(n_registros)
    
    st.dataframe(dados_mostrar, width="stretch")
    
    # Estatísticas descritivas
    st.subheader("📊 Estatísticas Descritivas")
    st.dataframe(dados_lag.describe(), width="stretch")
    
    # Download dos dados
    st.subheader("💾 Download dos Dados")
    csv = dados_mostrar.to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=csv,
        file_name=f'dados_climaticos_filtrados_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv',
    )

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        🌤️ Dashboard Climático INMET | Dados processados e analisados
        <br>
        Desenvolvido com Streamlit e Plotly
    </div>
    """, 
    unsafe_allow_html=True
)
