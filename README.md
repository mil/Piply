Pisample
========

Interface for both audio playback and recording on the Raspberry Pi. More info to come!

Main Modes / Capbilities:
------------------------------
- Filebrowser (Lib)
    * Access multiple media mounts
        - Specify hooks for mounting each source
        - I.e. Mount USB before accessing
        - I.e. Mount host to folder via SSHfs before accessing
    * File browser 
        - First folder (optionally) select by letter A-Z
        - Nested folders simple Up and Down browser
        - Play individual MP3/FLAC/WAV
        - Play stream files
        - Play albums (contents of a folder / a m3u playlist)
- Now Playing (Now)
    * Pause / Play
    * Seek back and forward 
    * Pitch up and down
    * Timestretch - Slow/Speed samples w/o affecting pitch
    * NO Queue support beyond 1 Album/File/Sample at a time
    * Skip current track
- Sampler (Smp)
    * Record samples from PCM / Line In
    * Playback samples
    * All manipulations in (Now) available in playback
- Config (Cfg)
    * Audio Volume Control


Hardware:
---------
- Raspberry Pi ($35)
- Adafruit i2c 16x2 RGB LCD Pi Plate ($20)
- (Optional) USB Audio Interface/Mixer ($30)
    * Behringer 302USB
