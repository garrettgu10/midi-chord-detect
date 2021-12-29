import pygame
import pygame.midi
from music21 import *

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

def describe_note(note_id):
    n = note.Note(note_id)
    return n.name

def describe_notes(notes):
    return list(map(describe_note, notes))

def describe_chord(notes):
    ch = chord.Chord(notes)
    return ch.pitchedCommonName

def main():
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    clock = pygame.time.Clock()

    running = True
    
    pygame.midi.init()

    if pygame.midi.get_count() == 0:
        print("No MIDI devices detected")
        exit()
    
    default_id = pygame.midi.get_default_input_id()
    print("Device: " + str(pygame.midi.get_device_info(default_id)))
    input = pygame.midi.Input(default_id)

    notes = set()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while input.poll():
            event = input.read(1)[0][0]
            if event[0] == 144:
                notes.add(event[1])
                print("Notes: " + str(describe_notes(notes)))
                print("Chord: " + str(describe_chord(notes)))
            elif event[0] == 128:
                notes.remove(event[1])
        
        clock.tick(144)

    input.close()
    pygame.midi.quit()
    pygame.font.quit()
    pygame.quit()

if __name__ == '__main__':
    main()