Piply - Rpi + LCD + Buttons + Your Music
=========================================
![Piply UI](http://userbound.com/things/Piply/piply.gif)

This is a simple UI for audio playback on the the Raspberry Pi. Built atop the [Adafruit i2c 16x2 LCD Pi Plate](http://www.adafruit.com/products/1115). UI built in Python2. Depends on Adafruit's `Adafruit_CharLCDPlate` and `mplayer.py`. Transforms your Raspberry Pi into standalone music playback device. 

3 Main Menus 
------------
### Library (Lib)
This is your basic filebrowsing interface. The first set of folders is selected A-Z. Then afterwords it's a standard up/down menu selection. If the folder you are in either: has no children folders or has an M3U playlist, you will be given an option to `Play Album`w contents.

Assumes your music is in the file format of:
- Music
    * Artist A
        - Album 1
            * Song.mp3
            * Song2.mp3
        - Album 2
        - Album 3
    * Artist B
    * Artist C

### Now Playing (Now)
Controls currently playing song.  The playback mode is based on mplayer and only one song may be playing at a time. There is no 'queue' beyond selecting to play an album contents. Supported playback operations include: pause/play, seek forward/back, speed up/down, skip.

### Configuration (Cfg )
As of now, the only configuration option that's supported is adjusting Alsa's master volume up and down. 

Setup
-----
- Ensure user is in `audio` group.
- Set music library path (may be USB / Network mount / etc)
- Ensure user is in group for `i2c_dev`


Upgrading Your Audio Interface
------------------------------
The sound quality in the Pi is pretty atrocious by default. If your want to upgrade your sound interface, I recomend the [Behringer 302USB](). It's a nice little cheap USB mixer. Piply plays nice with any alsa PCM, you just will need to set the default audio interface to a negative index ensuring the USB interface is recognized first:

` snd command`
