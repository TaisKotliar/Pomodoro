import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PomodoroTimer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost",True)
        self.root.geometry("450x250")
        self.root.configure(bg='#FA8072')
        self.root.title("Pomodoro timer")
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file = resource_path("tomato.png")))

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font = ("Ubuntu", 16))
        self.s.configure("TButton", font = ("Ubuntu", 16))
        
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill = 'both', pady = 10, padx = 10, expand = True)

        self.tab1 = ttk.Frame(self.tabs, width = 600, height = 100)
        self.tab2 = ttk.Frame(self.tabs, width = 600, height = 100)
        self.tab3 = ttk.Frame(self.tabs, width = 600, height = 100)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text = '25:00', font = ("Ubuntu", 40))
        self.pomodoro_timer_label.pack(pady = 20)

        self.short_break_timer_label = ttk.Label(self.tab2, text = '05:00', font = ("Ubuntu", 40))
        self.short_break_timer_label.pack(pady = 20)

        self.long_break_timer_label = ttk.Label(self.tab3, text = '15:00', font = ("Ubuntu", 40))
        self.long_break_timer_label.pack(pady = 20)

        self.tabs.add(self.tab1, text = ' Pomodoro ')
        self.tabs.add(self.tab2, text = ' Short break ')
        self.tabs.add(self.tab3, text = ' Long break ') 

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady = 10)

        self.start_button = ttk.Button(self.grid_layout, text = "Start", command = self.start_timer_thread)
        self.start_button.grid(row = 0, column = 0)

        self.skip_button = ttk.Button(self.grid_layout, text = "Skip", command = self.skip_clock)
        self.skip_button.grid(row = 0, column = 1)

        self.reset_button = ttk.Button(self.grid_layout, text = "Reset", command = self.reset_clock)
        self.reset_button.grid(row = 0, column = 2)

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text = "Pomodoros: 0", font = ("Ubuntu", 16), foreground="red")
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3)

        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    def start_timer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
        
        if timer_id == 1:
            full_seconds = 60 * 25
            
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()

        elif timer_id == 2:
            full_seconds = 60 * 5
            
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
                
        elif timer_id == 3:
            full_seconds = 60 * 15

            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        else:
            print("Invalid timer ID")
            
    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text = "25:00")
        self.short_break_timer_label.config(text = "05:00")
        self.long_break_timer_label.config(text = "15:00")
        self.pomodoro_counter_label.config(text = "Pomodoros: 0")
        self.running = False

    def skip_clock(self):
        
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0:
            self.pomodoro_timer_label.config(text = "25:00")
        elif current_tab == 1:
            self.short_break_timer_label.config(text = "05:00")
        elif current_tab == 2:
            self.long_break_timer_label.config(text = "15:00")
        
        self.stopped = True
        self.skipped = True

PomodoroTimer()