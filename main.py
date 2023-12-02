from genetic import genetic_algorithm
import pygame
import time
from midiutil import MIDIFile
import random

# Define a dictionary to map note names to MIDI pitch values
note_mapping = {
    'F3':53,'#F3':54,'G3':55,'#G3':56,'A3':57,'#A3':58,'B3':59,'C4':60, '#C4':61,'D4':62,'#D4':63,'E4':64,
    'F4':65,'#F4':66,'G4':67,'#G4':68,'A4':69,'#A4':70,'B4':71,'C5':72, '#C5':73,'D5':74,'#D5':75,'E5':76,
    'F5':77,'#F5':78,'G5':79
}

def melody_to_midi(melody, output_file="output.mid", tempo=120):
    # Create a MIDIFile object
    midi = MIDIFile(1)  # 1 track
    midi.addTempo(0, 0, tempo)

    i=0
    length=len(melody)
    while i<length:
        note_name=melody[i]
        if note_name=='0' or note_name=='-':
            i+=1
            continue
        duration = 1
        j=i+1
        while j<length and melody[j]=='-':
            j+=1
            duration+=1

        pitch=note_mapping[note_name]
        midi.addNote(0, 0, pitch, i, duration, 100)
        i+=duration
    return midi


if __name__ == "__main__":
    # 生成音乐
    melody = genetic_algorithm(pop_size=10, melody_length=16, generations=100)

    # 保存音乐
    midi = melody_to_midi(melody)
    with open("melody.mid", "wb") as output_file:
        midi.writeFile(output_file)

    # 播放音乐
    pygame.mixer.init()
    pygame.mixer.music.load("melody.mid")
    pygame.mixer.music.play()
    time.sleep(20)
    pygame.mixer.music.stop()
