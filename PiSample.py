#!/usr/bin/env python
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class PiSample:
    lcd  = None
    last_button = None
    mode = "main"
    main_mode_selected_index = 0
    main_mode_options = ("cmd", "lib", "pls")

    def __init__(self):
        self.lcd = Adafruit_CharLCDPlate()
        self.lcd.clear()
        self.mode_main_menu()
        self.loop()

    # Main Mode
    def mode_main_menu(self):
        message = "pisample\n"
        for index, option in enumerate(self.main_mode_options):
            if index == self.main_mode_selected_index:
                message += "*"
            else:
                message += " "
            message += option
            message += " "
        self.lcd.clear()
        self.lcd.message(message)

    def mode_main_btn(self, btn):
        if btn == "left" and self.main_mode_selected_index != 0:
            self.main_mode_selected_index -= 1
        if btn == "right" and self.main_mode_selected_index + 1 != len(self.main_mode_options):
            self.main_mode_selected_index += 1
        self.mode_main_menu()


    # Button Handler
    def button_press(self, btn):
        if self.mode is "main":
            self.mode_main_btn(btn)
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
