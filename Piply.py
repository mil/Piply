#!/usr/bin/env python2
from time import sleep
import os, sys, datetime, tempfile
import alsaaudio
sys.path.insert(0, './modules')
from Adafruit.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from mplayer import Player

class Piply:
    player, player.exec_path = Player(), "/usr/bin/mplayer"
    letters = (
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            )
    lcd, last_button, mode, seconds_counter, curr_char = None, None, "main", 0, 0

    main_mode_selected_index, main_mode_options = 0, ("Now", "Lib", "Cfg")
    now_mode_returns_to, now_mode_pitch_seek = 'main', 'seek'
    lib_mode_current_items =  ()
    lib_mode_root_dir, lib_mode_current_dir = "/mnt/media", "/mnt/media"
    lib_mode_scroll_position, lib_mode_letter_position = 0, 0
    lib_mode_selecting_letter, lib_mode_arrow_position_top = True, True

    def __init__(self):
        self.lcd = Adafruit_CharLCDPlate()
        self.lcd.clear()
        self.mode_main_menu()
        #self.mode_char_test()
        self.loop() 

    def marquee_text(self, text, chars_width):
        if len(text) < chars_width:
            return text
        chars_to_scroll = len(text) - chars_width
        offset = int(chars_to_scroll * (float(self.seconds_counter) / float(5)))
        if offset + chars_width > len(text):
            return text[0: chars_width - 1]
        return text[offset: offset + chars_width]

    def secs_to_formatted(self, secs):
        secs, mins = int(secs), 0
        while secs >= 60:
            mins += 1
            secs -= 60
        mins, secs = str(mins),  str(secs)
        if len(secs) == 1:
            secs = "0" + secs
        return mins + ":" + secs


    def mode_char_test(self):
        self.lcd.clear()
        symb = chr(self.curr_char)
        self.lcd.message("Chr " + str(self.curr_char) + " " + symb)
        self.curr_char += 1


    # Main Mode
    def mode_main_menu(self):
        message = "  "
        if self.player.filename != None:
            message += "P " if self.player.paused else "> "
        else:
            message += "  "
        message += ".Piply,.\n"
        for index, option in enumerate(self.main_mode_options):
            if index == self.main_mode_selected_index:
                message += " " + str(chr(126))
            else:
                message += "  "
            message += option + ""
        self.lcd.clear()
        self.lcd.message(message)

    def mode_main_btn(self, btn):
        if btn == "select":
            self.set_mode(self.main_mode_options[self.main_mode_selected_index])
            return
        if btn == "left" and self.main_mode_selected_index != 0:
            self.main_mode_selected_index -= 1
        if btn == "right" and self.main_mode_selected_index + 1 != len(self.main_mode_options):
            self.main_mode_selected_index += 1
        self.mode_main_menu()



    # Lib Mode -- filebrowser
    def mode_lib_menu(self): 
        message = ""

        if self.lib_mode_current_dir == self.lib_mode_root_dir and self.lib_mode_selecting_letter:
            message += "^ "
            for idx, letter in enumerate(self.letters):
                message += ("\nv " if idx == 13 else "")
                message += ((str(chr(126)) + letter.upper()) if self.lib_mode_letter_position == idx else letter)    
        else:
            # Only show current letter for artist
            row_1, row_2, top_fh, bottom_fh = "", "", "", ""

            def is_playing(fh):
                return self.player.filename == fh

            if self.lib_mode_arrow_position_top:
                row_1 += (str(chr(126)))
                top_fh = self.lib_mode_current_items[self.lib_mode_scroll_position]
            else:
                row_1 += " "
                if self.lib_mode_scroll_position != 0:
                    top_fh = self.lib_mode_current_items[self.lib_mode_scroll_position - 1]

            
            if not self.lib_mode_arrow_position_top:
                row_2 += (str(chr(126)))
                bottom_fh = self.lib_mode_current_items[self.lib_mode_scroll_position]
            else:
                row_2 += " "
                if self.lib_mode_scroll_position != len(self.lib_mode_current_items) - 1:
                    bottom_fh = self.lib_mode_current_items[self.lib_mode_scroll_position + 1]

            row_1 += self.marquee_text(top_fh, 15) if self.lib_mode_arrow_position_top else top_fh
            row_2 += self.marquee_text(bottom_fh, 15) if not self.lib_mode_arrow_position_top else bottom_fh 

            #if is_playing(top_fh):
            #    row_1 += "P" if self.player.paused else ">"
            #if is_playing(bottom_fh):
            #    row_2 += "P" if self.player.paused else ">"
            if len(row_1) > 16:
                row_1 = row_1[0:15]
            if len(row_2) > 16:
                row_2 = row_2[0:15]

            message = row_1 + "\n" + row_2
            
        self.lcd.clear()
        self.lcd.message(message)

    def mode_lib_btn(self, btn):
        if self.lib_mode_selecting_letter:
            # Selecting Top level letter
            if btn == "down":
                self.lib_mode_letter_position = min(self.lib_mode_letter_position + 1, 25)
            if btn == "up":
                self.lib_mode_letter_position = max(self.lib_mode_letter_position - 1, 0)
            if btn == "select":
                self.lib_mode_selecting_letter = False
                self.lib_mode_arrow_position_top = True
                self.lib_mode_scroll_position = 0
                self.seconds_counter = 0
                self.lib_mode_current_items = sorted(os.listdir(self.lib_mode_current_dir))
            if btn == "left":
                self.set_mode("main")
                return
        else:
            # File browser
            if btn == "down" and self.lib_mode_scroll_position != len(self.lib_mode_current_items) - 1:
                self.lib_mode_scroll_position += 1
                self.lib_mode_arrow_position_top = False
                self.seconds_counter = 0

            if btn == "up" and self.lib_mode_scroll_position != 0:
                self.lib_mode_scroll_position -= 1
                self.lib_mode_arrow_position_top = True
                self.seconds_counter = 0

            if btn == "select" or btn == "right":
                if self.lib_mode_current_items[self.lib_mode_scroll_position] == "Play Album":
                    self.play_audio(self.lib_mode_current_dir + "/")
                    return
                elif os.path.isfile(self.lib_mode_current_dir + "/" + self.lib_mode_current_items[self.lib_mode_scroll_position]):
                    self.play_audio(self.lib_mode_current_dir + "/" + self.lib_mode_current_items[self.lib_mode_scroll_position])
                    return
                else:
                    self.lib_mode_current_dir += "/" + self.lib_mode_current_items[self.lib_mode_scroll_position]
                    self.lib_mode_current_items = sorted(os.listdir(self.lib_mode_current_dir))
                    if os.path.isfile(self.lib_mode_current_dir + "/" + self.lib_mode_current_items[0]):
                        self.lib_mode_current_items.insert(0, "Play Album")
                    self.lib_mode_scroll_position = 0
                    self.lib_mode_arrow_position_top = True

            if btn == "left":
                if self.lib_mode_current_dir == self.lib_mode_root_dir and self.lib_mode_selecting_letter == False:
                    self.lib_mode_selecting_letter = True
                else:
                    self.lib_mode_arrow_position_top = True
                    self.lib_mode_scroll_position = 0
                    self.lib_mode_current_dir = os.path.abspath(os.path.join(self.lib_mode_current_dir + "/.."))
                    self.lib_mode_current_items = sorted(os.listdir(self.lib_mode_current_dir))

        if self.lib_mode_current_dir == self.lib_mode_root_dir:
            def only_current_letter(x):
                return x[0].lower() == self.letters[self.lib_mode_letter_position]
            self.lib_mode_current_items = sorted(filter(only_current_letter, self.lib_mode_current_items))

        self.mode_lib_menu()

    def mode_now_menu(self):
        if self.player.length == None or self.player.time_pos == None:
            self.set_mode(self.now_mode_returns_to)
            return

        line_1, line_2 = "", ""
        metadata = self.player.metadata or {}
        artist = metadata.get('Artist', '')
        album = metadata.get('Album', '')
        year = metadata.get('Year', '')
        title = metadata.get('Title', '')

        line_1 += "> " if not self.player.paused else "P "
        line_1 += self.marquee_text(title + " - " + artist + ", " + album + "(" + year + ") ", 14)

        line_2 += str(chr(126)) if self.now_mode_pitch_seek == "seek" else ""
        line_2 += self.secs_to_formatted(self.player.time_pos) + "/"
        line_2 += self.secs_to_formatted(self.player.length) + " "
        line_2 += str(chr(126)) if self.now_mode_pitch_seek == "speed" else ""
        line_2 += str("%.2f" % self.player.speed) + "x"

        self.lcd.clear()
        self.lcd.message(line_1 + "\n" + line_2)

    def mode_now_btn(self, btn):
        if btn == "left":
            self.set_mode(self.now_mode_returns_to)
            return

        if self.now_mode_pitch_seek == "seek":
            if btn == "down": 
                if self.player.time_pos <= 2:
                    self.player.time_pos = 0
                else:
                    self.player.time_pos -= 2
            if btn == "up" and self.player.time_pos + 2 < self.player.length:
                self.player.time_pos += 2
            if btn == "right":
                self.now_mode_pitch_seek = "speed"
            if btn == "select":
                self.player.pause()
    
        elif self.now_mode_pitch_seek == "speed":
            if btn == "down" or  btn == "up":
                self.player.speed += (0.02 if btn == "up" else -0.02)
            if btn == "select":
                self.player.speed = 1
            if btn == "right":
                self.now_mode_pitch_seek = "seek"

        self.mode_now_menu()


    def mode_smp_menu(self):
        self.lcd.clear()
        self.lcd.message("sampler")
    def mode_smp_btn(self, btn):
        if btn == "left":
            self.set_mode("main")


    def mode_cfg_menu(self):
        message = ""

        message += "Vol "
        message += str(int(alsaaudio.Mixer("PCM").getvolume()[0]))
        message += "%"

        self.lcd.clear()
        self.lcd.message(message)

    def mode_cfg_btn(self, btn):
        if btn == "left":
            self.set_mode("main")
        if btn == "up" or btn == "down":
            v = int(alsaaudio.Mixer("PCM").getvolume()[0])
            v += 2 if btn == "up" else -2
            v = min(max(0,v), 100)
            alsaaudio.Mixer("PCM").setvolume(v, 0)

        self.mode_cfg_menu()

    def play_audio(self, fp):
        # Plays audio and sets mode to Now
        if os.path.isfile(fp):
            self.player.loadfile(fp)
            sleep(0.2)
        else:
            playlist = tempfile.NamedTemporaryFile(delete=False)
            with playlist as temp_file:
                for idx, f in enumerate(sorted(os.listdir(fp))):
                    temp_file.write(fp + f + "\n")
            self.player.loadlist(playlist.name, 0)
            sleep(0.2)
            os.remove(playlist.name)

        if self.player.paused != False:
            self.player.pause()

        self.set_mode("Now")

    def redraw_menu(self):
        {
            "main" : self.mode_main_menu,
            "Now"  : self.mode_now_menu,
            "Lib"  : self.mode_lib_menu,
            "Cfg"  : self.mode_cfg_menu
        }[self.mode]()

    def set_mode(self, new_mode):
        self.now_mode_returns_to = self.mode
        self.mode = new_mode
        self.redraw_menu()

    # Button Handler
    def button_press(self, btn):
        if self.mode == "main":
            self.mode_main_btn(btn)
        elif self.mode == "Now":
            self.mode_now_btn(btn)
        elif self.mode == "Lib":
            self.mode_lib_btn(btn)
        elif self.mode == "Cfg":
            self.mode_cfg_btn(btn)
        elif self.mode == "Smp":
            self.mode_smp_btn(btn)

    def loop(self):
        last_date = datetime.datetime.now()
        while True:
            now = datetime.datetime.now()
            difference = now - last_date
            mins_secs = divmod(difference.days * 86400 + difference.seconds, 60)

            self.seconds_counter += mins_secs[0] * 60
            self.seconds_counter += mins_secs[1]
            if self.seconds_counter >= 6:
                self.seconds_counter = 0

            if mins_secs[0] > 0 or mins_secs[1] > 0.8:
                last_date = now
                self.redraw_menu()




            current_button = None
            btn_map = {
                    self.lcd.LEFT : "left",
                    self.lcd.RIGHT : "right",
                    self.lcd.UP: "up",
                    self.lcd.DOWN: "down",
                    self.lcd.SELECT: "select"
                    }
            for k in btn_map:
                if (self.lcd.buttonPressed(k)):
                    current_button = btn_map[k]
            if current_button != None and current_button != self.last_button:
                self.button_press(current_button)
            self.last_button = current_button



Piply()
