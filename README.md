Piply
=====

Interface for audio playback on the the Raspberry Pi. Built atop the Adafruit i2c 16x2 LCD Pi Plate. Intended to transform Raspberry Pi into standalone music playback device. 

Modes / Capbilities:
--------------------
- Filebrowser (Lib)
    * (Optionally) First folder select by letter A-Z
        - Intended for browsing Artists
    * Nested folders simple Up, Down, Select browser
    * Play individual MP3/FLAC/WAV
    * Play stream files
    * Play albums 
        - (m3u playlist or contents of folder in alphabetical order)
- Now Playing (Now)
    * Pause / Play
    * Seek back and forward 
    * Speed up and down music
    * Skip current track
- Config (Cfg)
    * Audio Volume Control

Hardware:
---------
- Raspberry Pi ($35)
- Adafruit i2c 16x2 RGB LCD Pi Plate ($20)
- (Optional) USB Audio Interface/Mixer ($30)
    * Behringer 302USB
