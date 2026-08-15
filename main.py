import librosa
import music21
import pretty_midi
import crepe

midi_data = pretty_midi.PrettyMIDI('love-story.mid')

print("--- MIDI Metadata ---")
print("Estimated BPM:", midi_data.estimate_tempo())
print("Duration:", midi_data.get_end_time())
print("Total Instruments", midi_data.instruments)

print("\n--- Detected Tracks/Instruments ---")
for i, instrument in enumerate(midi_data.instruments):
    is_drum = " (Drums)" if instrument.is_drum else ""
    print(f" Track {i+1}: {instrument.name or 'Unnamed'} | Program: {instrument.program} | Notes: {len(instrument.notes)}{is_drum}")
# for i, instrument in enumerate(midi_data.instruments):
#     if instrument.is_drum:
#         is_drum = " (Drums)"
#     else:
#         is_drum = ""
#     print(f" Track {i+1}: {instrument.name or 'Unnamed'} | Program: {instrument.program} | Notes: {len(instrument.notes)}{is_drum}")
# total_velocity = sum(sum(midi_data.get_chroma()))
# print("Relative Velocity:", [sum(semitone)/total_velocity for semitone in midi_data.get_chroma()])
