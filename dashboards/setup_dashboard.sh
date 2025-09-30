#!/bin/bash

# Script para configurar e executar o dashboard climático

echo "🌤️ Configurando Dashboard Climático"
echo "=================================="

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Por favor, instale o Python3."
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado. Criando novo ambiente..."
    python3 -m venv venv
else
    echo "✅ Usando ambiente virtual existente..."
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install streamlit plotly pandas numpy scikit-learn seaborn matplotlib joblib

# Verificar se os dados existem
if [ ! -f "Dados do INEP que eu solicitei/dados_A707_D_2014-01-01_2025-05-01.csv" ]; then
    echo "⚠️  Aviso: Arquivo de dados não encontrado no caminho esperado."
    echo "   Verifique se o arquivo existe em: 'Dados do INEP que eu solicitei/dados_A707_D_2014-01-01_2025-05-01.csv'"
fi

echo ""
echo "✅ Configuração concluída!"
echo ""
echo "🚀 Para executar o dashboard:"
echo "   1. Ative o ambiente virtual: source venv/bin/activate"
echo "   2. Execute: streamlit run dashboard_streamlit.py"
echo ""
echo "🌐 O dashboard será aberto no navegador em: http://localhost:8501"
echo ""

# Perguntar se deseja executar agora
read -p "Deseja executar o dashboard agora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Iniciando dashboard..."
    streamlit run dashboard_streamlit.py
fi
