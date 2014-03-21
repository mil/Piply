Pisample
========
This is a tool for DIY music production, under heavy development, but basically this will serve to act as a filebrowser/sampler/playback device. The interface will sample (from line-in) and be able to playback those samples or files from the filebrowser and pitch up/down (major feature). I may also add in some Sox effects to apply to samples.

Interface Modes / Capbilities:
------------------------------
- Filebrowser (Mnt)
    * Access multiple media mounts
        - Specify hooks to mount each source
        - I.e. Mount USB before accessing
        - I.e. Mount host to folder via SSHfs before accessing
    * File browser 
        - First folder select by letter A-Z
        - Nested folders simple Up and Down browser
        - Play individual MP3/FLAC/WAV
        - Play stream files
        - Play albums (all contents of folder / from m3u playlist)
- Playback (Aud)
    * Pause / Play
    * Seek back and forward
    * Pitch up and down
    * NO Queue support beyond 1 Album/File/Sample at a time
    * Backend mplayer
- Sampler (Smpl)
    * Record samples from Audio Interface Line In
    * (Maybe) Apply Sox Effects to Samples
    * Playback Samples

Hardware:
---------
- Raspberry Pi ($35)
- Adafruit i2c 16x2 RGB LCD Pi Plate ($20)
- USB Audio Interface/Mixer ($50)
