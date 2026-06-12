import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import tkintermapview
import sqlite3
import regex as re
from geopy.geocoders import Nominatim
from R4SM_lib import app, controler, model, view

if __name__ == '__main__':
    main_app = app.App()
    main_app.run()