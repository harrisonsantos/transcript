import streamlit as st
import os
import subprocess
import whisper
import tempfile
import shutil
from pathlib import Path
import time

# Configuração da página
st.set_page_config(
    page_title="Transcritor de Vídeos",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .step-box {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .success-box {
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #d4edda;
        color: #155724;
    }
    .error-box {
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Função para verificar se o FFmpeg está disponível
@st.cache_resource
def check_ffmpeg():
    try:
        # Tenta diferentes caminhos possíveis do FFmpeg
        ffmpeg_paths = ["ffmpeg", "/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg"]
        
        for path in ffmpeg_paths:
            try:
                result = subprocess.run([path, "-version"], capture_output=True, check=True, timeout=10)
                return True, path
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        return False, None
    except Exception as e:
        return False, None

# Função para instalar FFmpeg se necessário (para ambiente local)
def install_ffmpeg_instructions():
    return """
    ⚠️ **FFmpeg não encontrado no sistema!**
    
    **Se você está executando localmente:**
    
    **Windows:**
    1. Baixe: https://ffmpeg.org/download.html
    2. Extraia e adicione ao PATH
    
    **Linux/Ubuntu:**
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```
    
    **macOS:**
    ```bash
    brew install ffmpeg
    ```
    
    **Se você está no Streamlit Cloud:**
    - Verifique se o arquivo `packages.txt` está no repositório
    - Conteúdo do `packages.txt` deve ser:
    ```
    ffmpeg
    libsm6
    libxext6
    libfontconfig1
    libxrender1
    ```
    - Faça commit e aguarde o redeploy
    """

# Função para extrair áudio do vídeo
def extract_audio(video_path, audio_path, ffmpeg_path="ffmpeg"):
    try:
        ffmpeg_command = [
            ffmpeg_path, "-y", "-i", video_path,
            "-vn", "-acodec", "mp3", "-ab", "192k",
            "-loglevel", "error",  # Reduz logs verbosos
            audio_path
        ]
        result = subprocess.run(
            ffmpeg_command, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=300  # 5 minutos de timeout
        )
        return True, "Áudio extraído com sucesso!"
    except subprocess.TimeoutExpired:
        return False, "Timeout: O vídeo é muito longo para processar"
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao extrair áudio: {e.stderr}"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

# Função para transcrever áudio
@st.cache_resource
def load_whisper_model(model_size):
    """Carrega o modelo Whisper (com cache para evitar recarregamento)"""
    return whisper.load_model(model_size)

def transcribe_audio(audio_path, model_size="medium", language="pt"):
    try:
        model = load_whisper_model(model_size)
        result = model.transcribe(audio_path, language=language)
        return True, result["text"]
    except Exception as e:
        return False, f"Erro na transcrição: {str(e)}"

# Função principal
def main():
    # Cabeçalho
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Transcritor de Vídeos</h1>
        <p>Converta seus vídeos em texto de forma simples e rápida</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar com configurações
    st.sidebar.title("⚙️ Configurações")
    
    # Seleção do modelo Whisper
    model_size = st.sidebar.selectbox(
        "Qualidade da Transcrição:",
        ["tiny", "base", "small", "medium", "large"],
        index=3,
        help="Modelos maiores são mais precisos, mas mais lentos"
    )
    
    # Seleção do idioma
    language = st.sidebar.selectbox(
        "Idioma do Vídeo:",
        ["pt", "en", "es", "fr", "de", "it"],
        index=0,
        help="Selecione o idioma principal do vídeo"
    )

    # Informações sobre os modelos
    model_info = {
        "tiny": "Mais rápido, menor precisão",
        "base": "Rápido, precisão básica",
        "small": "Balanceado",
        "medium": "Boa precisão (recomendado)",
        "large": "Máxima precisão, mais lento"
    }
    
    st.sidebar.info(f"**Modelo selecionado:** {model_size}\n\n{model_info[model_size]}")

    # Verificar se FFmpeg está disponível
    ffmpeg_available, ffmpeg_path = check_ffmpeg()
    
    if not ffmpeg_available:
        st.error("❌ **FFmpeg não encontrado!**")
        st.markdown(install_ffmpeg_instructions())
        
        # Adicionar botão para tentar recarregar
        if st.button("🔄 Tentar novamente"):
            st.rerun()
        
        return

    # Upload do arquivo
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.subheader("📁 Passo 1: Fazer Upload do Vídeo")
    
    uploaded_file = st.file_uploader(
        "Selecione seu arquivo de vídeo",
        type=['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'],
        help="Formatos suportados: MP4, AVI, MOV, WMV, FLV, WebM, MKV"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        # Mostrar informações do arquivo
        file_size = uploaded_file.size / (1024 * 1024)  # MB
        st.info(f"**Arquivo:** {uploaded_file.name} ({file_size:.2f} MB)")

        # Botão para processar
        if st.button("🚀 Iniciar Transcrição", type="primary"):
            
            # Criar diretório temporário
            with tempfile.TemporaryDirectory() as temp_dir:
                
                # Salvar arquivo de vídeo
                video_path = os.path.join(temp_dir, uploaded_file.name)
                with open(video_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Barra de progresso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Passo 1: Extrair áudio
                status_text.text("🔄 Extraindo áudio do vídeo...")
                progress_bar.progress(25)
                
                audio_path = os.path.join(temp_dir, "audio.mp3")
                success, message = extract_audio(video_path, audio_path, ffmpeg_path)
                
                if not success:
                    st.error(f"❌ {message}")
                    return
                
                # Passo 2: Transcrever áudio
                status_text.text("🎤 Transcrevendo áudio... (isso pode demorar alguns minutos)")
                progress_bar.progress(50)
                
                success, transcription = transcribe_audio(
                    audio_path, 
                    model_size=model_size, 
                    language=language
                )
                
                if not success:
                    st.error(f"❌ {transcription}")
                    return
                
                # Passo 3: Finalizar
                status_text.text("✅ Transcrição concluída!")
                progress_bar.progress(100)
                
                # Mostrar resultado
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.subheader("📝 Resultado da Transcrição")
                st.text_area(
                    "Texto transcrito:",
                    transcription,
                    height=300,
                    help="Você pode selecionar e copiar o texto"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Botão de download
                st.download_button(
                    label="📥 Baixar Transcrição (.txt)",
                    data=transcription,
                    file_name=f"transcricao_{uploaded_file.name.split('.')[0]}.txt",
                    mime="text/plain"
                )
                
                # Estatísticas
                word_count = len(transcription.split())
                char_count = len(transcription)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Palavras", word_count)
                with col2:
                    st.metric("Caracteres", char_count)
                with col3:
                    st.metric("Modelo Usado", model_size.upper())

    # Instruções na sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Como usar:")
    st.sidebar.markdown("""
    1. **Configure** o modelo e idioma
    2. **Faça upload** do seu vídeo
    3. **Clique** em "Iniciar Transcrição"
    4. **Aguarde** o processamento
    5. **Baixe** o resultado
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Informações:")
    st.sidebar.markdown("""
    - **Formatos suportados:** MP4, AVI, MOV, WMV, FLV, WebM, MKV
    - **Tamanho máximo:** 200MB (limite do Streamlit)
    - **Idiomas:** Português, Inglês, Espanhol, Francês, Alemão, Italiano
    - **Tecnologia:** OpenAI Whisper
    """)

if __name__ == "__main__":
    main()