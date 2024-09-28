

import tkinter as tk
from tkcalendar import Calendar

def update_selected_date():
    selected_date.config(text="Selected Date: " + cal.get_date())

root = tk.Tk()
root.title("Calendar App")
root.geometry("400x400")

cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.pack(pady=20)

selected_date = tk.Label(root, text="")
selected_date.pack(pady=10)

cal.bind("<<CalendarSelected>>", lambda event: update_selected_date())

root.mainloop()