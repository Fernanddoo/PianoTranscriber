import os
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import pretty_midi
import matplotlib.pyplot as plt
import numpy as np

def cleanup_midi_data(pm_object, min_note_duration=0.1):
    print("🧹 Otimizando MIDI...")
    
    # cria um novo objeto PrettyMIDI para receber os dados limpos
    # limpa sujeiras na separação do audio
    cleaned_pm = pretty_midi.PrettyMIDI()
    
    for instrument in pm_object.instruments:
        # definindo de padrao, no caso, piano "acustico"
        piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        new_instrument = pretty_midi.Instrument(program=piano_program)
        
        # filtragem das notas
        for note in instrument.notes:
            duration = note.end - note.start
            if duration >= min_note_duration:
                new_instrument.notes.append(note)
        
        cleaned_pm.instruments.append(new_instrument)
        
    return cleaned_pm

# aqui utilizo o modelo e escolho os parametros dele
def audio_to_midi(audio_path, output_midi_path):
    print(f"Transcrevendo: {audio_path}...")
    
    # parametros do modelo
    model_output, midi_data, note_events = predict(
        audio_path,
        ICASSP_2022_MODEL_PATH,
        onset_threshold=0.68,   
        frame_threshold=0.3,
        minimum_note_length=127.7,
        minimum_frequency=27.5,
        maximum_frequency=4186.0,
        multiple_pitch_bends=False,
        melodia_trick=False
    )
    
    # limpa o MIDI antes de salva
    refined_midi = cleanup_midi_data(midi_data, min_note_duration=0.12)
    # e salva
    refined_midi.write(output_midi_path)
    return refined_midi
