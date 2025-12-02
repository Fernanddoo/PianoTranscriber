import pretty_midi
import matplotlib.pyplot as plt
import numpy as np
import io

# testei diversas ferramentas de para transcrever midi para partitura, mas nenhuma é consistente
# aderi a renderizar o MIDI diretamente, pois ainda é possível aprender a tocar ela por esse formato
def generate_piano_roll_image(midi_path):
    # carrega o MIDI
    pm = pretty_midi.PrettyMIDI(midi_path)
    
    # gera a matriz do piano roll 
    # fs=100 significa 100 frames por segundo
    piano_roll = pm.get_piano_roll(fs=100)
    
    # recorta para mostrar as teclas do piano, geralmente as mais utilizadas (MIDI 21 a 108)
    # isso remove o espaço vazio de notas muito graves ou muito agudas
    piano_roll = piano_roll[21:108, :]
    
    # calcula dimensões proporcionais
    duration_sec = pm.get_end_time()
    # largura fixa, altura baseada na duração
    # aspect ratio ajustado para leitura vertical
    plt.figure(figsize=(12, duration_sec / 5)) 
    
    # desenha o MIDI
    # origin='lower' coloca as notas graves embaixo
    # cmap='inferno' ou 'magma' dá aquele visual "fogo" bonito
    plt.imshow(piano_roll, aspect='auto', origin='lower', cmap='magma')
    
    plt.title(f"Visualização das Notas (Duração: {duration_sec:.1f}s)")
    plt.xlabel("Tempo (frames)")
    plt.ylabel("Teclas do Piano (Grave -> Agudo)")
    
    # salva em memóriaem vez de arquivo
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    buf.seek(0)
    plt.close()
    
    return buf