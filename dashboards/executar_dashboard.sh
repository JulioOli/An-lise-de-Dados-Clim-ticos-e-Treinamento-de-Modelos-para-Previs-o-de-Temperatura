#!/bin/bash

# Script simplificado para executar o dashboard no ambiente virtual existente

echo "🌤️ Executando Dashboard Climático"
echo "================================="

# Verificar se estamos no diretório correto
if [ ! -f "dashboard_streamlit.py" ]; then
    echo "❌ Arquivo dashboard_streamlit.py não encontrado."
    echo "   Execute este script no diretório do projeto."
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado."
    echo "   Certifique-se de que o ambiente virtual 'venv' existe no diretório."
    exit 1
fi

# Verificar se o Streamlit está instalado
if [ ! -f "venv/bin/streamlit" ]; then
    echo "📦 Instalando Streamlit no ambiente virtual existente..."
    ./venv/bin/pip install streamlit plotly statsmodels
    
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências."
        exit 1
    fi
fi

echo "🚀 Iniciando dashboard..."
echo "📊 O dashboard será aberto em: http://localhost:8501"
echo ""
echo "💡 Para parar o dashboard, pressione Ctrl+C"
echo ""

# Executar o dashboard
./venv/bin/streamlit run dashboard_streamlit.py
