import music21

us = music21.environment.UserSettings()

musescore_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'

us['musescoreDirectPNGPath'] = musescore_path
us['musicxmlPath'] = musescore_path

# music21.environment.set(
#     'musescoreDirectPath',
#     '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
# )

print("MuseScore path configured successfully!")