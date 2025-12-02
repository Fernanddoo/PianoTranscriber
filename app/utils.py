import os
import subprocess
import glob

def get_demucs_cmd():
    return "demucs"

def download_youtube_audio(url, output_dir="outputs"):
    # limpa URL se tiver timestamp ou playlists acopladas
    if "&" in url: url = url.split("&")[0]
    
    print(f"Baixando: {url}")
    
    # template com id
    output_template = f"{output_dir}/%(id)s.%(ext)s"

    # flags críticas para evitar erro 403 do yt
    # o yt me bloqueava, achava que era spam ou bot
    cmd = [
        "yt-dlp", 
        url, 
        "-x", "--audio-format", "mp3", "--audio-quality", "192K",
        "-o", output_template, 
        "--restrict-filenames", 
        "--no-check-certificate", 
        "--quiet",
        "--rm-cache-dir",  
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        # tenta auto-update se falhar
        print("Erro 403 ou falha detectada. Tentando auto-update do yt-dlp...")
        subprocess.run(["yt-dlp", "-U"], check=False)
        subprocess.run(cmd, check=True)

    # pega o arquivo mais recente criado na pasta
    list_of_files = glob.glob(f'{output_dir}/*.mp3') 
    if not list_of_files:
        raise FileNotFoundError("O download parece ter falhado (nenhum arquivo MP3 encontrado).")
        
    final_path = max(list_of_files, key=os.path.getctime)
    return final_path

def separate_audio(audio_path, output_dir="outputs/separated"):
    if not os.path.exists(audio_path): 
        raise FileNotFoundError(f"Arquivo não encontrado: {audio_path}")
    
    os.makedirs(output_dir, exist_ok=True)

    demucs_executable = get_demucs_cmd()
    
    # htdemucs_6s é o modelo que separa os instrumentos e esse pode separa em vários instrumentos
    cmd = [demucs_executable, "-n", "htdemucs_6s", "--mp3", "-o", output_dir, audio_path]
    
    print(f"Separando faixas: {audio_path}")
    subprocess.run(cmd, check=True)
    
    # estrutura de pastas do Demucs: outputs/htdemucs/NOME_DA_MUSICA/instrumento.mp3
    filename = os.path.basename(audio_path)
    base_name = os.path.splitext(filename)[0]
    target_dir = os.path.join(output_dir, "htdemucs_6s", base_name)
    
    # retorna somente o piano, que é o que importa, mas tem essas outras opcoes
    # as vzs pode estar no "other" o piano
    return {
        #"drums": os.path.join(target_dir, "drums.mp3"),
        #"bass": os.path.join(target_dir, "bass.mp3"),
        #"guitar": os.path.join(target_dir, "guitar.mp3"),
        "piano": os.path.join(target_dir, "piano.mp3"),   
        #"vocals": os.path.join(target_dir, "vocals.mp3"),
        "other": os.path.join(target_dir, "other.mp3")
    }