from genetic import genetic_algorithm
import pygame
import time
from midiutil import MIDIFile

def melody_to_midi(melody, output_file="output.mid", tempo=120):
    # Create a MIDIFile object
    midi = MIDIFile(1)  # 1 track
    midi.addTempo(0, 0, tempo)

    # Define a dictionary to map note names to MIDI pitch values
    note_mapping = {'C': 60,'4C': 61, 'D': 62,'4D': 63,'E': 64, 'F': 65,'4F':66, 'G': 67,'4G':68, 'A': 69,'4A':70, 'B': 71}

    # Add notes to the MIDI file
    for i, note in enumerate(melody):
        # Extract note name and duration from the melody
        note_name, duration = note[:-1], int(note[-1])

        # Map note name to MIDI pitch
        pitch = note_mapping[note_name]

        # Add note to the MIDI file
        midi.addNote(0, 0, pitch, i, duration, 100)

    # Return the MIDI object
    return midi

if __name__ == "__main__":
    # 生成音乐
    melody = genetic_algorithm(pop_size=100, melody_length=20, generations=50)

    # 保存音乐
    midi = melody_to_midi(melody)
    with open("melody.mid", "wb") as output_file:
        midi.writeFile(output_file)

    # 播放音乐
    pygame.mixer.init()
    pygame.mixer.music.load("melody.mid")
    pygame.mixer.music.play()
    time.sleep(10)
    pygame.mixer.music.stop()
