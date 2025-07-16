# 🎬 Transcritor de Vídeos

Uma aplicação web simples e intuitiva para transcrever vídeos em texto usando OpenAI Whisper.

## 🚀 Funcionalidades

- **Interface amigável**: Feita com Streamlit, não requer conhecimento técnico
- **Múltiplos formatos**: Suporta MP4, AVI, MOV, WMV, FLV, WebM, MKV
- **Vários idiomas**: Português, Inglês, Espanhol, Francês, Alemão, Italiano
- **Diferentes qualidades**: 5 modelos Whisper disponíveis (tiny a large)
- **Download fácil**: Baixe a transcrição em formato .txt
- **Estatísticas**: Contagem de palavras e caracteres

## 🛠️ Como usar

1. **Acesse a aplicação** (link do Streamlit Cloud)
2. **Configure** o modelo de transcrição e idioma na barra lateral
3. **Faça upload** do seu arquivo de vídeo
4. **Clique** em "Iniciar Transcrição"
5. **Aguarde** o processamento (pode demorar alguns minutos)
6. **Visualize** o resultado na tela
7. **Baixe** o arquivo de transcrição

## 📋 Requisitos do Sistema

- FFmpeg (instalado automaticamente no Streamlit Cloud)
- Python 3.8+
- Conexão com internet

## 🔧 Instalação Local

```bash
# Clone o repositório
git clone [seu-repositorio]
cd transcritor-videos

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

## 📊 Modelos Disponíveis

| Modelo | Tamanho | Velocidade | Precisão |
|--------|---------|------------|----------|
| tiny   | ~39 MB  | Muito rápido | Básica |
| base   | ~74 MB  | Rápido | Boa |
| small  | ~244 MB | Moderado | Muito boa |
| medium | ~769 MB | Lento | Excelente |
| large  | ~1550 MB| Muito lento | Máxima |

## 🌐 Deploy no Streamlit Cloud

Para fazer deploy da sua própria versão:

1. **Faça fork** deste repositório
2. **Acesse** [share.streamlit.io](https://share.streamlit.io)
3. **Conecte** sua conta GitHub
4. **Selecione** seu repositório
5. **Configure** o arquivo principal como `app.py`
6. **Faça deploy**

## 📄 Estrutura do Projeto

```
transcritor-videos/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências Python
├── packages.txt        # Pacotes do sistema
└── README.md          # Documentação
```

## 🔒 Privacidade

- Os arquivos são processados temporariamente
- Nenhum dado é armazenado permanentemente
- Os arquivos são deletados após o processamento

## 🐛 Problemas Conhecidos

- Arquivos muito grandes podem causar timeout
- Modelos maiores podem demorar muito para carregar
- Algumas extensões de vídeo podem não funcionar

## 📞 Suporte

Para problemas ou sugestões, abra uma issue no repositório do GitHub.

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🙏 Agradecimentos

- OpenAI pelo modelo Whisper
- Streamlit pela plataforma web
- FFmpeg pelo processamento de vídeo