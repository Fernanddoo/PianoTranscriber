import streamlit as st
import os
from utils import download_youtube_audio, separate_audio
from transcribe import audio_to_midi 
from renderer import generate_piano_roll_image

st.set_page_config(page_title="Piano MIDI Transcriber", layout="wide", page_icon="🎹")

st.title("🎹 Piano Transcriber")
st.caption("Transforme vídeos do YouTube em arquivos MIDI para aprender a tocar.")

url = st.text_input("Cole o link do YouTube:", placeholder="https://youtube.com/...")

if st.button("Gerar MIDI") and url:
    status = st.status("🚀 Iniciando o motor...", expanded=True)
    
    try:
        # download
        status.write("📥 Baixando áudio...")
        raw_path = download_youtube_audio(url, "outputs")
        
        # separação 
        status.write("🧹 Isolando a faixa de Piano (Demucs)...")
        stems = separate_audio(raw_path, "outputs/separated")
        piano_track = stems['piano']
        
        # transcrição 
        status.write("🎼 Transcrevendo notas (Basic Pitch)...")
        midi_filename = os.path.basename(raw_path).replace(".mp3", ".mid")
        midi_path = os.path.join("outputs", midi_filename)
        
        # gera o MIDI otimizado
        audio_to_midi(piano_track, midi_path)
        
        status.update(label="✅ MIDI Gerado com Sucesso!", state="complete", expanded=False)
        
        # renderiza o resultado da transcricao
        st.divider()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🎧 Áudio & Download")
            
            st.markdown("**1. Ouça o Piano Isolado:**")
            st.audio(piano_track, format='audio/mp3')
            
            st.markdown("**2. Baixe o MIDI:**")
            st.caption("Importe este arquivo no Synthesia, Musescore ou sua DAW favorita.")
            with open(midi_path, "rb") as f:
                st.download_button(
                    label="⬇️ Baixar Arquivo .MID",
                    data=f,
                    file_name=midi_filename,
                    mime="audio/midi"
                )

        with col2:
            st.subheader("👀 O que a IA escutou")
            st.caption("Gráfico das notas (Grave embaixo, Agudo em cima)")
            
            # Gera e exibe o Piano Roll
            with st.spinner("Gerando visualização gráfica..."):
                image_buf = generate_piano_roll_image(midi_path)
                st.image(image_buf, use_container_width=True)

    except Exception as e:
        status.update(label="❌ Erro", state="error")
        st.error(f"Ocorreu um erro: {e}")