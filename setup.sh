#!/bin/bash

# Script de configuração para Streamlit Cloud
# Este script é executado automaticamente durante o deploy

echo "🔄 Configurando ambiente..."

# Criar diretório .streamlit se não existir
mkdir -p ~/.streamlit/

# Verificar se FFmpeg está disponível
echo "🔍 Verificando FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg encontrado: $(which ffmpeg)"
    ffmpeg -version | head -1
else
    echo "❌ FFmpeg não encontrado!"
    echo "Tentando instalar via apt..."
    
    # Para ambientes baseados em Debian/Ubuntu
    if command -v apt &> /dev/null; then
        apt update
        apt install -y ffmpeg
    fi
fi

# Verificar se as dependências Python estão instaladas
echo "🔍 Verificando dependências Python..."
python -c "import whisper; print('✅ Whisper instalado')" 2>/dev/null || echo "❌ Whisper não encontrado"
python -c "import torch; print('✅ PyTorch instalado')" 2>/dev/null || echo "❌ PyTorch não encontrado"
python -c "import streamlit; print('✅ Streamlit instalado')" 2>/dev/null || echo "❌ Streamlit não encontrado"

echo "🎉 Configuração concluída!"