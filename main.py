# main.py
import tkinter as tk
from calendar_gui import CalendarApp

root = tk.Tk()
root.geometry("1000x1000")
app = CalendarApp(root)
root.mainloop()
