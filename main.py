import librosa
import music21
import pretty_midi
import crepe
import os

midi_data = pretty_midi.PrettyMIDI('love-story.mid')

print("--- MIDI Metadata ---")
print("Estimated BPM:", midi_data.estimate_tempo())
print("Duration:", midi_data.get_end_time())
print("Total Instruments", midi_data.instruments)

print("\n--- Detected Tracks/Instruments ---")
for i, instrument in enumerate(midi_data.instruments):
    is_drum = " (Drums)" if instrument.is_drum else ""
    print(f" Track {i+1}: {instrument.name or 'Unnamed'} | Program: {instrument.program} | Notes: {len(instrument.notes)}{is_drum}")

active_notes = []
for instrument in midi_data.instruments:
    if not instrument.is_drum and len(instrument.notes) > 49: active_notes.extend(instrument.notes)

active_notes.sort(key=lambda x: x.start)

treble_notes = []
bass_notes = []

lower_bound = 53
upper_bound = 67

# Sorting using floating threshold
for note in active_notes:
    # Clear treble
    if note.pitch > upper_bound:
        treble_notes.append(note) 
    # CLear bass
    elif note.pitch < lower_bound:
        bass_notes.append(note)
    # Middle zone
    else:
        concurrent_notes = []

        for n in active_notes:
            if abs(n.start - note.start) < 0.05 and n != note:
                concurrent_notes.append(n)

        if concurrent_notes:
            # Average pitch of concurrent notes (played at the same time)
            avg_pitch = sum(n.pitch for n in concurrent_notes) / len(concurrent_notes)

            bass_notes.append(note) if note.pitch < avg_pitch else treble_notes.append(note)
        else:
            # If played alone, use middle C split
            bass_notes.append(note) if note.pitch < 60 else treble_notes.append(note)

new_midi = pretty_midi.PrettyMIDI()

# Two piano tracks
right_hand = pretty_midi.Instrument(program=0, name="Right Hand (Treble)")
left_hand = pretty_midi.Instrument(program=0, name="Left Hand (Bass)")

right_hand.notes = treble_notes
left_hand.notes = bass_notes

new_midi.instruments.append(right_hand)
new_midi.instruments.append(left_hand)
new_midi.write("new_piano.mid")

print("Saved new MIDI file successfully!")

def export_piano_staff(midi_file_path, output_xml="piano_staff.musicxml"):
    score = music21.converter.parse(midi_file_path)

    # Extract parts and group into a Grand staff
    parts = score.getElementsByClass(music21.stream.Part)

    if len(parts) >= 2:
        rh_part = parts[0]
        lh_part = parts[1]

        rh_part.insert(0, music21.clef.TrebleClef())
        lh_part.insert(0, music21.clef.BassClef())

        rh_part.partName = "Right Hand"
        lh_part.partName = "Left Hand"

        staff_group = music21.layout.StaffGroup([rh_part, lh_part], name="Piano", abbreviation="Pno.")
        staff_group.symbol = 'brace'
        staff_group.barTogether = True
    
        score.insert(0, staff_group)

    # Quantization aka rhythmic alignment (subdivisions of quarter notes)
    score = score.quantize([4, 8, 16], processOffsets=True)

    # Key analysis
    key_sig = score.analyze('key')
    score.insert(0, key_sig)

    score.write('musicxml', fp=output_xml)

# Export to PDF or PNG
# def musicxml_to_pdf_or_png(xml_filepath, output_format="pdf"):
#     musescore_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
#     music21.environment.set('musescoreDirectPNGPath', musescore_path)
#     music21.environment.set('musicxmlPath', musescore_path) 

#     score = music21.converter.parse(xml_filepath)
    
#     if output_format.lower() == "pdf":
#         # Render to PDF
#         output_path = xml_filepath.replace(".musicxml", ".pdf")
#         score.write('musicxml.pdf', fp=output_path)
#         print(f"Exported PDF to {output_path}")
        
#     elif output_format.lower() == "png":
#         # Render to PNG
#         output_path = xml_filepath.replace(".musicxml", ".png")
#         score.write('musicxml.png', fp=output_path)
#         print(f"Exported PNG to {output_path}")

def musicxml_to_pdf_or_png(xml_filepath, output_format="pdf"):
    musescore_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
    
    # Generate output filename
    output_path = xml_filepath.replace(".musicxml", f".{output_format.lower()}")
    
    # Run the exact CLI command that worked in your terminal
    cmd = [musescore_path, "-o", output_path, xml_filepath]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Successfully generated {output_format.upper()}: {output_path}")
    except subprocess.CalledProcessError as e:
        print("MuseScore failed with error:")
        print(e.stderr)

export_piano_staff("new_piano.mid", output_xml="piano_staff.musicxml")

script_dir = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(script_dir, "piano_staff.musicxml")

# Run conversion
musicxml_to_pdf_or_png("piano_staff.musicxml", output_format="pdf")