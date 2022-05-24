from mido import MidiFile, MidiTrack, Message
import os

DEBUG = True

path = "files/"

midis = []
if DEBUG:
    midis.append(MidiFile(path + "_Twinkle_Little_Star.mid"))
else:
    for file in os.listdir(path):
        print("Loading file: " + file)
        if file.endswith(".mid"):
            midis.append(MidiFile(path + file, clip=True))

markov = {}
old = None

for midi in midis:
    for track in midi.tracks:
        for message in track:
            if message.type == "note_on":
                if message.note in markov and old is not None:
                    if old in markov[message.note]:
                        markov[message.note][old] += 1
                    else:
                        markov[message.note][old] = 1
                elif old is not None:
                    markov[message.note] = {old: 1}
                old = message.note

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)
max_notes = 100
current = list(markov.keys())[0]

for i in range(max_notes):
    track.append(Message(type="note_on", note=current, velocity=100, time=32))
    if current in markov:
        current = list(markov[current].keys())[0]
    else:
        current = list(markov.keys())[0]

mid.save("output.mid")
