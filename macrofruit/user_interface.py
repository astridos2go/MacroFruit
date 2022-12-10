import os
from tkinter import Tk
from tkinter.ttk import Button, Frame

import sv_ttk


class user_interface(Tk):
    def __init__(self, frozen, path, config):
        super().__init__()
        self.frozen = frozen
        self.path = path
        self.config = config

        self.app_title = "MacroFruit"
        self.iconbitmap(os.path.join(path, "images", "icon.ico"))

        sv_ttk.set_theme("light")
        self.title(self.app_title)

        self.showMacroPad()

    def showMacroPad(self):
        layout = self.config["macropad_layout"]
        rotation = layout["rotation"].get(int)

        button_size = 100

        if layout["default"].get(bool):
            r = 4
            c = 3

        else:
            r = layout["rows"].get(int)
            c = layout["columns"].get(int)

        if rotation in {90, 270}:
            ROWS = c
            COLUMNS = r

        else:
            ROWS = r
            COLUMNS = c

        self.buttons = []

        button_group = Frame(self)
        for r_ in range(ROWS):
            self.buttons.append([])
            for c_ in range(COLUMNS):
                # Create button frame to constrain size
                bframe = Frame(button_group, width=button_size, height=button_size)
                # Create button
                button = Button(bframe, text=f"{r_}, {c_}")

                # Set options to allow button to resize, but not frame
                bframe.grid_propagate(False)
                bframe.columnconfigure(0, weight=1)
                bframe.rowconfigure(0, weight=1)

                # Grid the button frame
                bframe.grid(row=r_, column=c_)
                # Grid the button, and make it expand
                button.grid(sticky="NWSE")
                # Save reference to button
                self.buttons[r_].append(button)

        self.screen = Frame(self, relief="solid", borderwidth=1)
        self.screen.grid_propagate(False)

        eframe = Frame(self, width=button_size, height=button_size)
        eframe.grid_propagate(False)
        eframe.columnconfigure(0, weight=1)
        eframe.rowconfigure(0, weight=1)
        self.encoder = Button(eframe)
        self.encoder.grid(sticky="NEWS")

        match rotation:
            case 0:
                # Screen is longways
                self.screen.config(width=(button_size * 2), height=button_size)

                self.screen.grid(row=0, column=0, columnspan=2)
                eframe.grid(row=0, column=2)
                button_group.grid(row=1, column=0, columnspan=COLUMNS, rowspan=ROWS)
            case 90:
                self.screen.config(width=button_size, height=(button_size * 2))

                button_group.grid(row=0, column=0, columnspan=COLUMNS, rowspan=ROWS)
                self.screen.grid(row=0, column=(COLUMNS + 1), rowspan=2)
                eframe.grid(row=2, column=(COLUMNS + 1))
            case 180:
                self.screen.config(width=(button_size * 2), height=button_size)

                button_group.grid(row=0, column=0, columnspan=COLUMNS, rowspan=ROWS)
                eframe.grid(row=(ROWS + 1), column=0)
                self.screen.grid(row=(ROWS + 1), column=1, columnspan=2)
            case 270:
                self.screen.config(width=button_size, height=(button_size * 2))

                eframe.grid(row=0, column=0)
                self.screen.grid(row=1, column=0, rowspan=2)
                button_group.grid(row=0, column=1, columnspan=COLUMNS, rowspan=ROWS)
