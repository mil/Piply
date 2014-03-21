#!/usr/bin/env python
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import os
import subprocess

class PiSample:
    letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
    lcd  = None
    last_button = None
    mode = "main"

    curr_char = 0

    main_mode_selected_index = 0
    main_mode_options = ("Lib", "Smpl", "Now")

    lib_mode_root_dir = "/mnt/x300"
    lib_mode_current_dir = "/mnt/x300"
    lib_mode_current_items =  ()
    lib_mode_scroll_position = 0
    lib_mode_letter_position = 0
    lib_mode_selecting_letter = True
    lib_mode_arrow_position_top = True

    def __init__(self):
        self.lcd = Adafruit_CharLCDPlate()
        self.lcd.clear()
        self.mode_main_menu()
        self.loop()

    def mode_char_test(self):
        self.lcd.clear()
        symb = chr(self.curr_char)
        self.lcd.message("Chr " + str(self.curr_char) + " " + symb)
        self.curr_char += 1

    # Main Mode
    def mode_main_menu(self):
        message = "pisample " + chr(226) + "\n"
        for index, option in enumerate(self.main_mode_options):
            if index == self.main_mode_selected_index:
                message += str(chr(126))
            else:
                message += " "
            message += option
            message += " "
        self.lcd.clear()
        self.lcd.message(message)

    def mode_main_btn(self, btn):
        if btn == "select":
            if self.main_mode_options[self.main_mode_selected_index] == "Lib":
                self.mode = "Lib"
                self.mode_lib_menu()
                return

        if btn == "left" and self.main_mode_selected_index != 0:
            self.main_mode_selected_index -= 1
        if btn == "right" and self.main_mode_selected_index + 1 != len(self.main_mode_options):
            self.main_mode_selected_index += 1
        self.mode_main_menu()



    def mode_lib_menu(self): 
        message = ""

        if self.lib_mode_current_dir == self.lib_mode_root_dir and self.lib_mode_selecting_letter:
            for idx, letter in enumerate(self.letters):
                message += ("  ^\n" if idx == 13 else "")
                message += (letter.upper() if self.lib_mode_letter_position == idx else letter)    
        else:
            # Only sow current letter for artist
            row_1 = ""
            row_2 = ""

            if self.lib_mode_arrow_position_top:
                row_1 = (str(chr(126))) + (self.lib_mode_current_items[self.lib_mode_scroll_position])[0:15]
            elif self.lib_mode_scroll_position != 0:
                row_1 = " " + (self.lib_mode_current_items[self.lib_mode_scroll_position - 1])[0:15]

            rwl = list(row_1)
            blank_space = len(rwl)
            if blank_space < 15:
                while blank_space <= 15:
                    rwl.append(" ")
                    blank_space+=1
            rwl[15] = "<"
            row_1 = "".join(rwl)


            if not self.lib_mode_arrow_position_top:
                row_2 = (str(chr(126))) + (self.lib_mode_current_items[self.lib_mode_scroll_position])[0:15]
            elif self.lib_mode_scroll_position != len(self.lib_mode_current_items) - 1:
                row_2 = " " + (self.lib_mode_current_items[self.lib_mode_scroll_position + 1])[0:15]

            message = row_1 + "\n" + row_2
            
        self.lcd.clear()
        self.lcd.message(message)

    def mode_lib_btn(self, btn):
        if self.lib_mode_selecting_letter:
            if btn == "right":
                self.lib_mode_letter_position = min(self.lib_mode_letter_position + 1, 25)
            if btn == "left":
                self.lib_mode_letter_position = max(self.lib_mode_letter_position - 1, 0)
            if btn == "select":
                self.lib_mode_selecting_letter = False
                self.lib_mode_arrow_position_top = True
                self.lib_mode_scroll_position = 0
                self.lib_mode_current_items = sorted(os.listdir(self.lib_mode_current_dir))
            if btn == "up":
                self.mode = "main"
                self.mode_main_menu()
                return


        else:
            if btn == "down" and self.lib_mode_scroll_position != len(self.lib_mode_current_items) - 1:
                self.lib_mode_scroll_position += 1
                self.lib_mode_arrow_position_top = False
            if btn == "up" and self.lib_mode_scroll_position != 0:
                self.lib_mode_scroll_position -= 1
                self.lib_mode_arrow_position_top = True
            if btn == "select" or btn == "right":
                if self.lib_mode_current_items[self.lib_mode_scroll_position] == "Play Album":
                    self.play_audio(self.lib_mode_current_dir + "/*")
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
    

    def play_audio(self, fp):
        self.lcd.clear()
        self.lcd.message("Playing!")
        subprocess.Popen(["/usr/bin/killall", "mplayer"], stdout = subprocess.PIPE)
        print "WOO"
        subprocess.Popen(["/usr/bin/mplayer", fp], stdout = subprocess.PIPE)
        print "Doo"

        

    # Button Handler
    def button_press(self, btn):
        if self.mode is "main":
            #self.mode_char_test()
            self.mode_main_btn(btn)
        elif self.mode is "Lib":
            self.mode_lib_btn(btn)
    def loop(self):
        while True:
            current_button = None
            if self.lcd.buttonPressed(self.lcd.LEFT):
                current_button = "left"
            if self.lcd.buttonPressed(self.lcd.RIGHT):
                current_button = "right"
            if self.lcd.buttonPressed(self.lcd.UP):
                current_button = "up"
            if self.lcd.buttonPressed(self.lcd.DOWN):
                current_button = "down"
            if self.lcd.buttonPressed(self.lcd.SELECT):
                current_button = "select"
            if current_button != None and current_button != self.last_button:
                self.button_press(current_button)
            self.last_button = current_button
PiSample()
