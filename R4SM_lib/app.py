import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
import tkintermapview
import sqlite3
import regex as re
from geopy.geocoders import Nominatim
from R4SM_lib import controler, model, view

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        print('init started')
        self.app_view = view.View(self)
        self.title('Rent 4 Sport')
        self.app_controller = controler.Controler(self.app_view,model)
        self.app_view.set_controler(self.app_controller)
        self.app_view.pack()
    
    def run(self):
        self.mainloop()
