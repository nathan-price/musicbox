# Music Box
# Nathan Price 2018

import midi
import os
import pygame, pygame.midi
import time

# Setup
pattern = midi.read_midifile("midi/mm/song-of-healing.mid")
print(pattern)
pygame.init()
pygame.midi.init()
port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)
midi_out.set_instrument(0)

# Note Events
NOTE_ON = 1
NOTE_OFF = 0
TEMPO = 2
def GetType(event):
    if type(event) == type(midi.NoteOnEvent(tick=0, velocity=0, pitch=0)):
        return NOTE_ON
    elif type(event) == type(midi.NoteOffEvent(tick=100, pitch=0)):
        return NOTE_OFF
    elif type(event) == type(midi.SetTempoEvent()):
        return TEMPO
    return -1

# Parse Song
events = []
for track in pattern:
    tick = 0
    for event in track:
        tick += event.tick
        etype = GetType(event)
        if etype == NOTE_ON or etype == NOTE_OFF:
            events.append({'tick':tick, 'type':etype, 'note':event.data[0], 'velocity':event.data[1], 'channel':event.channel})
        elif etype == TEMPO:
            tick_time = (int.from_bytes(event.data, 'big') / pattern.resolution) / 1000000.0
            events.append({'tick':tick, 'type':etype, 'time':tick_time})
events.sort(key = lambda x: x['tick'])

# Play Song
index = 0
tick = 0
ticktime = 0.0005
scale = 1
dsp = ""
prev = time.perf_counter()
now = prev
while index < len(events):
    if events[index]['tick'] <= tick:
        if events[index]['type'] == TEMPO:
            tick_time = events[index]['time']
        elif events[index]['type'] == NOTE_ON:
            midi_out.note_on(events[index]['note'], events[index]['velocity'], events[index]['channel'])
            dsp += midi.NOTE_VALUE_MAP_SHARP[events[index]['note']] + " "
            #dsp[events[index]['note']] = 'O'
        elif events[index]['type'] == NOTE_OFF:
            midi_out.note_off(events[index]['note'], events[index]['velocity'], events[index]['channel'])
            #dsp[events[index]['note']] = ' '
        index += 1
    else:
        if dsp != "":
            print(dsp)
            dsp = ""
        prev = now
        now = time.perf_counter()
        elapsed = (now - prev) * scale
        tick += elapsed / ticktime
        #scale = 0.4 * (1 + index / len(events))
