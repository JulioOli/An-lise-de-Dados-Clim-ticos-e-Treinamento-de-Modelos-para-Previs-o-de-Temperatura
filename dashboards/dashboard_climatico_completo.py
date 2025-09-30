"""
Dashboard Completo de Análise Climática
Integra dados do INMET com resultados de análises de modelos ML
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, dash_table
import joblib
from datetime import datetime, date
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Configuração de cores e estilo
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'success': '#F18F01',
    'warning': '#C73E1D',
    'light': '#F8F9FA',
    'dark': '#343A40',
    'pastel_blue': '#AED6F1',
    'pastel_green': '#A9DFBF',
    'pastel_orange': '#F9E79F',
    'pastel_red': '#F1948A'
}

class ClimateDataProcessor:
    """Classe para processamento dos dados climáticos"""
    
    def __init__(self):
        self.df_original = None
        self.df_with_lags = None
        self.model_results = None
        self.comparison_results = None
        self.improvements = None
        
    def load_data(self):
        """Carrega todos os datasets necessários"""
        try:
            # Dados originais do INMET
            inmet_path = "/home/iioulos/Documents/IC_Danilo-Cotozika/Dados do INEP que eu solicitei/dados_A707_D_2014-01-01_2025-05-01.csv"
            
            # Definir colunas
            colunas = [
                'data', 'precipitacao_total', 'pressao_atm_media', 
                'temp_orvalho_media', 'temp_maxima', 'temp_media', 
                'temp_minima', 'umidade_relativa_media', 
                'umidade_relativa_minima', 'umidade_relativa_maxima', 
                'vento_vel_media'
            ]
            
            # Carregar dados originais (pulando metadados)
            self.df_original = pd.read_csv(
                inmet_path,
                sep=',', 
                encoding='latin1',
                skiprows=11,
                header=None,
                names=colunas
            )
            
            # Converter data e limpar dados
            self.df_original['data'] = pd.to_datetime(self.df_original['data'])
            for col in self.df_original.columns:
                if col != 'data':
                    self.df_original[col] = pd.to_numeric(self.df_original[col], errors='coerce')
            
            # Interpolação de valores faltantes
            self.df_original = self.df_original.set_index('data')
            self.df_original = self.df_original.interpolate(method='time')
            self.df_original = self.df_original.reset_index()
            
            # Carregar dados com lag features
            self.df_with_lags = pd.read_csv("/home/iioulos/Documents/IC_Danilo-Cotozika/dados_climaticos_com_lags.csv")
            self.df_with_lags['data'] = pd.to_datetime(self.df_with_lags['data'])
            
            # Carregar resultados dos modelos
            self.model_results = pd.read_csv("/home/iioulos/Documents/IC_Danilo-Cotozika/model_comparison_results.csv", index_col=0)
            
            # Carregar comparação completa
            self.comparison_results = pd.read_csv("/home/iioulos/Documents/IC_Danilo-Cotozika/comparacao_lag_features_completa.csv")
            
            # Carregar melhorias
            self.improvements = pd.read_csv("/home/iioulos/Documents/IC_Danilo-Cotozika/melhorias_lag_features.csv")
            
            print("Dados carregados com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
    
    def add_derived_features(self):
        """Adiciona features derivadas aos dados"""
        # Adicionar estação do ano
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Verão'
            elif month in [3, 4, 5]:
                return 'Outono'
            elif month in [6, 7, 8]:
                return 'Inverno'
            else:
                return 'Primavera'
        
        self.df_original['estacao'] = self.df_original['data'].dt.month.apply(get_season)
        
        # Categorias de precipitação
        def categorize_precipitation(precip):
            if precip == 0:
                return 'Nenhuma'
            elif precip <= 2.5:
                return 'Leve'
            elif precip <= 10:
                return 'Moderada'
            else:
                return 'Pesada'
        
        self.df_original['categoria_precipitacao'] = self.df_original['precipitacao_total'].apply(categorize_precipitation)
        
        # Extremos de temperatura
        self.df_original['temp_extrema'] = (
            (self.df_original['temp_maxima'] > self.df_original['temp_maxima'].quantile(0.95)) |
            (self.df_original['temp_minima'] < self.df_original['temp_minima'].quantile(0.05))
        )

# Inicializar processador de dados
processor = ClimateDataProcessor()

# Carregar dados
if processor.load_data():
    processor.add_derived_features()
else:
    print("Falha ao carregar dados. Verificar caminhos dos arquivos.")

# Inicializar app Dash
app = dash.Dash(__name__)
app.title = "Dashboard Climático - Análise INMET"

# Layout principal
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🌤️ Dashboard de Análise Climática", 
                style={'textAlign': 'center', 'color': COLORS['primary'], 'marginBottom': '10px'}),
        html.P("Análise Completa dos Dados INMET e Modelos de Previsão", 
               style={'textAlign': 'center', 'color': COLORS['dark'], 'fontSize': '18px'})
    ], style={'backgroundColor': COLORS['light'], 'padding': '20px', 'marginBottom': '20px'}),
    
    # Tabs
    dcc.Tabs(id="main-tabs", value='overview', children=[
        dcc.Tab(label='📊 Visão Geral', value='overview'),
        dcc.Tab(label='🤖 Modelos ML', value='models'),
        dcc.Tab(label='📈 Séries Temporais', value='timeseries'),
        dcc.Tab(label='🔗 Correlação', value='correlation'),
        dcc.Tab(label='📊 Distribuições', value='distributions'),
        dcc.Tab(label='📉 Scatter Plots', value='scatter'),
        dcc.Tab(label='📋 Dados', value='data')
    ]),
    
    # Conteúdo das tabs
    html.Div(id='tab-content')
], style={'fontFamily': 'Arial, sans-serif'})

# Callbacks para conteúdo das tabs
@app.callback(Output('tab-content', 'children'), Input('main-tabs', 'value'))
def render_content(active_tab):
    if active_tab == 'overview':
        return create_overview_tab()
    elif active_tab == 'models':
        return create_models_tab()
    elif active_tab == 'timeseries':
        return create_timeseries_tab()
    elif active_tab == 'correlation':
        return create_correlation_tab()
    elif active_tab == 'distributions':
        return create_distributions_tab()
    elif active_tab == 'scatter':
        return create_scatter_tab()
    elif active_tab == 'data':
        return create_data_tab()

def create_overview_tab():
    """Cria a aba de visão geral"""
    if processor.df_original is None:
        return html.Div("Erro: Dados não carregados")
    
    df = processor.df_original
    
    # Métricas principais
    best_model = processor.model_results.loc[processor.model_results['R2'].idxmax()]
    total_records = len(df)
    avg_temp = df['temp_media'].mean()
    avg_humidity = df['umidade_relativa_media'].mean()
    
    # Cards de métricas
    metrics_cards = html.Div([
        html.Div([
            html.H3(f"{best_model['R2']:.3f}", style={'color': COLORS['primary'], 'margin': '0'}),
            html.P("Melhor R² (Gradient Boosting)", style={'margin': '5px 0 0 0'})
        ], className='metric-card', style={
            'backgroundColor': COLORS['pastel_blue'], 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),
        
        html.Div([
            html.H3(f"{total_records:,}", style={'color': COLORS['success'], 'margin': '0'}),
            html.P("Registros Analisados", style={'margin': '5px 0 0 0'})
        ], className='metric-card', style={
            'backgroundColor': COLORS['pastel_green'], 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),
        
        html.Div([
            html.H3(f"{avg_temp:.1f}°C", style={'color': COLORS['warning'], 'margin': '0'}),
            html.P("Temperatura Média", style={'margin': '5px 0 0 0'})
        ], className='metric-card', style={
            'backgroundColor': COLORS['pastel_orange'], 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),
        
        html.Div([
            html.H3(f"{avg_humidity:.1f}%", style={'color': COLORS['secondary'], 'margin': '0'}),
            html.P("Umidade Média", style={'margin': '5px 0 0 0'})
        ], className='metric-card', style={
            'backgroundColor': COLORS['pastel_red'], 'padding': '20px', 'borderRadius': '10px',
            'textAlign': 'center', 'width': '23%', 'display': 'inline-block', 'margin': '1%'
        })
    ], style={'marginBottom': '30px'})
    
    # Gráficos de pizza
    season_counts = df['estacao'].value_counts()
    precip_counts = df['categoria_precipitacao'].value_counts()
    
    fig_seasons = px.pie(
        values=season_counts.values, 
        names=season_counts.index,
        title="Distribuição de Dados por Estação",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig_precipitation = px.pie(
        values=precip_counts.values,
        names=precip_counts.index,
        title="Frequência de Precipitação",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    charts_row = html.Div([
        html.Div([
            dcc.Graph(figure=fig_seasons)
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(figure=fig_precipitation)
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ])
    
    return html.Div([metrics_cards, charts_row])

def create_models_tab():
    """Cria a aba de modelos ML"""
    if processor.model_results is None:
        return html.Div("Erro: Resultados dos modelos não carregados")
    
    # Gráfico de comparação de modelos
    fig_comparison = go.Figure()
    
    # RMSE
    fig_comparison.add_trace(go.Bar(
        name='RMSE',
        x=processor.model_results.index,
        y=processor.model_results['RMSE'],
        yaxis='y',
        offsetgroup=1,
        marker_color=COLORS['warning']
    ))
    
    # R²
    fig_comparison.add_trace(go.Bar(
        name='R²',
        x=processor.model_results.index,
        y=processor.model_results['R2'],
        yaxis='y2',
        offsetgroup=2,
        marker_color=COLORS['primary']
    ))
    
    fig_comparison.update_layout(
        title='Comparação de Performance dos Modelos',
        xaxis_title='Modelos',
        yaxis=dict(title='RMSE', side='left'),
        yaxis2=dict(title='R²', side='right', overlaying='y'),
        barmode='group'
    )
    
    # Tabela de ranking
    ranking_table = dash_table.DataTable(
        data=processor.model_results.round(4).reset_index().to_dict('records'),
        columns=[
            {'name': 'Modelo', 'id': 'index'},
            {'name': 'RMSE', 'id': 'RMSE'},
            {'name': 'R²', 'id': 'R2'}
        ],
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': COLORS['primary'], 'color': 'white'},
        style_data_conditional=[
            {
                'if': {'row_index': processor.model_results['R2'].argmax()},
                'backgroundColor': COLORS['pastel_green'],
                'color': 'black',
            }
        ]
    )
    
    # Gráfico de melhorias com lag features
    if processor.improvements is not None:
        fig_improvements = go.Figure()
        
        fig_improvements.add_trace(go.Bar(
            name='Melhoria RMSE (%)',
            x=processor.improvements['Modelo'],
            y=processor.improvements['Melhoria_RMSE_%'],
            marker_color=COLORS['success']
        ))
        
        fig_improvements.update_layout(
            title='Melhoria dos Modelos com Lag Features',
            xaxis_title='Modelos',
            yaxis_title='Melhoria RMSE (%)'
        )
    
    return html.Div([
        html.H3("Performance dos Modelos ML"),
        dcc.Graph(figure=fig_comparison),
        
        html.H3("Ranking de Performance"),
        ranking_table,
        
        html.H3("Impacto das Lag Features"),
        dcc.Graph(figure=fig_improvements) if processor.improvements is not None else html.P("Dados de melhoria não disponíveis")
    ])

def create_timeseries_tab():
    """Cria a aba de séries temporais"""
    if processor.df_original is None:
        return html.Div("Erro: Dados não carregados")
    
    return html.Div([
        html.H3("Análise de Séries Temporais"),
        
        html.Div([
            html.Label("Selecione as variáveis:"),
            dcc.Dropdown(
                id='timeseries-variables',
                options=[
                    {'label': 'Temperatura Média', 'value': 'temp_media'},
                    {'label': 'Umidade Relativa', 'value': 'umidade_relativa_media'},
                    {'label': 'Pressão Atmosférica', 'value': 'pressao_atm_media'},
                    {'label': 'Precipitação', 'value': 'precipitacao_total'}
                ],
                value=['temp_media', 'umidade_relativa_media'],
                multi=True
            )
        ], style={'width': '48%', 'margin': '20px 0'}),
        
        dcc.Graph(id='timeseries-plot')
    ])

@app.callback(
    Output('timeseries-plot', 'figure'),
    Input('timeseries-variables', 'value')
)
def update_timeseries(selected_vars):
    if not selected_vars or processor.df_original is None:
        return go.Figure()
    
    df = processor.df_original
    fig = go.Figure()
    
    colors = [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['secondary']]
    
    for i, var in enumerate(selected_vars):
        fig.add_trace(go.Scatter(
            x=df['data'],
            y=df[var],
            mode='lines',
            name=var.replace('_', ' ').title(),
            line=dict(color=colors[i % len(colors)])
        ))
    
    fig.update_layout(
        title='Séries Temporais das Variáveis Selecionadas',
        xaxis_title='Data',
        yaxis_title='Valores',
        hovermode='x unified'
    )
    
    return fig

def create_correlation_tab():
    """Cria a aba de correlação"""
    if processor.df_original is None:
        return html.Div("Erro: Dados não carregados")
    
    # Correlação entre variáveis principais
    numeric_cols = ['temp_media', 'temp_minima', 'temp_maxima', 'umidade_relativa_media', 
                   'pressao_atm_media', 'precipitacao_total', 'vento_vel_media']
    
    corr_matrix = processor.df_original[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Mapa de Correlação entre Variáveis Climáticas",
        color_continuous_scale='RdBu_r'
    )
    
    # Correlação com lag features (se disponível)
    lag_content = html.Div("Dados de lag features não disponíveis")
    
    if processor.df_with_lags is not None:
        lag_cols = [col for col in processor.df_with_lags.columns if '_lag' in col]
        if lag_cols:
            lag_corr = processor.df_with_lags[lag_cols + ['temp_media']].corr()['temp_media'].sort_values(ascending=False)
            
            fig_lag_corr = go.Figure(data=go.Bar(
                x=lag_corr.index[1:11],  # Top 10 correlações (excluindo auto-correlação)
                y=lag_corr.values[1:11],
                marker_color=COLORS['success']
            ))
            
            fig_lag_corr.update_layout(
                title='Top 10 Correlações com Lag Features',
                xaxis_title='Lag Features',
                yaxis_title='Correlação com Temperatura Média',
                xaxis_tickangle=-45
            )
            
            lag_content = dcc.Graph(figure=fig_lag_corr)
    
    return html.Div([
        html.H3("Análise de Correlação"),
        dcc.Graph(figure=fig_corr),
        
        html.H3("Correlação com Lag Features"),
        lag_content
    ])

def create_distributions_tab():
    """Cria a aba de distribuições"""
    if processor.df_original is None:
        return html.Div("Erro: Dados não carregados")
    
    df = processor.df_original
    
    # Histograma de temperatura
    fig_temp_hist = px.histogram(
        df, x='temp_media', nbins=50,
        title='Distribuição da Temperatura Média',
        color_discrete_sequence=[COLORS['primary']]
    )
    
    # Histograma de umidade
    fig_humidity_hist = px.histogram(
        df, x='umidade_relativa_media', nbins=50,
        title='Distribuição da Umidade Relativa',
        color_discrete_sequence=[COLORS['success']]
    )
    
    # Box plot de temperatura por estação
    fig_temp_box = px.box(
        df, x='estacao', y='temp_media',
        title='Temperatura por Estação',
        color='estacao',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Densidade de precipitação
    fig_precip_density = px.histogram(
        df[df['precipitacao_total'] > 0], x='precipitacao_total',
        title='Densidade de Precipitação (dias com chuva)',
        nbins=50,
        color_discrete_sequence=[COLORS['warning']]
    )
    
    return html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=fig_temp_hist)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig_humidity_hist)], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ]),
        
        html.Div([
            html.Div([dcc.Graph(figure=fig_temp_box)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig_precip_density)], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ])

def create_scatter_tab():
    """Cria a aba de scatter plots"""
    if processor.df_original is None:
        return html.Div("Erro: Dados não carregados")
    
    df = processor.df_original
    
    # Temperatura vs Umidade
    fig_temp_humidity = px.scatter(
        df, x='temp_media', y='umidade_relativa_media',
        title='Temperatura vs Umidade',
        color='estacao',
        color_discrete_sequence=px.colors.qualitative.Set3,
        trendline="ols"
    )
    
    # Pressão vs Temperatura
    fig_pressure_temp = px.scatter(
        df, x='pressao_atm_media', y='temp_media',
        title='Pressão vs Temperatura',
        color='estacao',
        color_discrete_sequence=px.colors.qualitative.Set3,
        trendline="ols"
    )
    
    # Precipitação vs Umidade
    fig_precip_humidity = px.scatter(
        df, x='precipitacao_total', y='umidade_relativa_media',
        title='Precipitação vs Umidade',
        color='categoria_precipitacao',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Previsto vs Real (usando melhor modelo se disponível)
    scatter_predicted = html.Div("Gráfico de predição vs real não disponível (modelo não carregado)")
    
    return html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=fig_temp_humidity)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(figure=fig_pressure_temp)], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ]),
        
        html.Div([
            html.Div([dcc.Graph(figure=fig_precip_humidity)], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([scatter_predicted], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ])

def create_data_tab():
    """Cria a aba de dados brutos"""
    if processor.df_original is None:
        return html.Div("Erro: Dados não carregados")
    
    df = processor.df_original.copy()
    
    # Preparar dados para a tabela
    df_display = df.round(2)
    df_display['data'] = df_display['data'].dt.strftime('%Y-%m-%d')
    
    return html.Div([
        html.H3("Dados Brutos Interativos"),
        
        html.Div([
            html.Label("Filtrar por período:"),
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date=df['data'].min(),
                end_date=df['data'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'margin': '20px 0'}),
        
        dash_table.DataTable(
            id='data-table',
            columns=[{"name": col, "id": col} for col in df_display.columns],
            data=df_display.head(100).to_dict('records'),  # Primeiros 100 registros
            page_size=20,
            sort_action="native",
            filter_action="native",
            style_cell={'textAlign': 'center', 'fontSize': '12px'},
            style_header={'backgroundColor': COLORS['primary'], 'color': 'white'},
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{temp_extrema} = True',
                        'column_id': ['temp_minima', 'temp_maxima', 'temp_media']
                    },
                    'backgroundColor': COLORS['pastel_red'],
                    'color': 'black',
                }
            ]
        )
    ])

if __name__ == '__main__':
    print("Iniciando Dashboard Climático...")
    print("Acesse: http://localhost:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
