import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import re
from tkinter import *
from tkinter import font as tkFont
import os

def open_calendar():
    os.system("python kalendars3.py")

def execute_query(query, parameters=()):
    conn = sqlite3.connect('doktorats.db')
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

def add_person_to_database(first_name, last_name, birth_year, personal_code, phone_number):
    existing_person = find_person_by_personal_code(personal_code)
    
    if existing_person:
        return f"Persona ar personas kodu {personal_code} jau ir datubāzē"
    
    query = 'INSERT INTO people (first_name, last_name, birth_year, personal_code, phone_number) VALUES (?, ?, ?, ?, ?)'
    execute_query(query, (first_name, last_name, birth_year, personal_code, phone_number))
    return "Persona pievienota datubāzei"

def find_person_by_personal_code(personal_code):
    query = 'SELECT * FROM people WHERE personal_code=?'
    return execute_query(query, (personal_code,))

def register_for_person(person_id, id_diena, id_laiks, id_fvp):
    query = 'INSERT INTO registration (person_id, id_diena, id_laiks, id_fvp) VALUES (?, ?, ?, ?)'
    execute_query(query, (person_id, id_diena, id_laiks, id_fvp))

def get_person_register(person_id):
    query = 'SELECT person_id, id_diena, id_laiks, id_fvp FROM registration WHERE person_id = ?'
    return execute_query(query, (person_id,))

def delete_class_registration(person_id, registration_id):
    query = 'DELETE FROM registration WHERE person_id = ? AND id = ?'
    execute_query(query, (person_id, registration_id))

# GUI funkcijas
def add_person_window():
    def submit():
        first_name = first_name_entry.get().strip().title()
        last_name = last_name_entry.get().strip().title()
        birth_year = birth_year_entry.get()
        personal_code = personal_code_entry.get()
        phone_number = phone_number_entry.get()
        

        if not re.fullmatch(r'^[a-zA-ZāčēģīķļņšūžĀČĒĢĪĶĻŅŠŪŽ\s]+$', first_name):
            messagebox.showerror("Kļūda", "Vārdā jābūt tikai burtiem no latīnu, vai latvieši alfabēta.")
            return
        
        if not re.fullmatch(r'^[a-zA-ZāčēģīķļņšūžĀČĒĢĪĶĻŅŠŪŽ\s]+$', last_name):
            messagebox.showerror("Kļūda", "Vārdā jābūt tikai burtiem no latīnu, vai latvieši alfabēta.")
            return
        
        
        if not re.fullmatch(r'\d{6}-\d{5}', personal_code):
            messagebox.showerror("Kļūda", "Personas kodam jābūt formātā: 6 cipari, svītriņa, 5 cipari (piemēram, 123456-78901).")
            return
        
        

        if not re.fullmatch(r'^\d{4}$', birth_year):
            messagebox.showerror("Kļūda", "Dzimšanas gadam jābūt tikai četriem cipariem.")
            return
        
        if not re.fullmatch(r'^\d{8}$', phone_number):
            messagebox.showerror("Kļūda", "Telefona numuram jābūt tikai astoņiem cipariem.")
            return
        
        result = add_person_to_database(first_name, last_name, birth_year, personal_code, phone_number)
        messagebox.showinfo("Pievienošana", result)

    
    window = tk.Toplevel()
    window.title("Pievienot cilvēku")
    
    tk.Label(window, text="Vārds").grid(row=0, column=0)
    first_name_entry = tk.Entry(window)
    first_name_entry.grid(row=0, column=1)
    
    tk.Label(window, text="Uzvārds").grid(row=1, column=0)
    last_name_entry = tk.Entry(window)
    last_name_entry.grid(row=1, column=1)
    
    tk.Label(window, text="Dzimšanas gads").grid(row=2, column=0)
    birth_year_entry = tk.Entry(window)
    birth_year_entry.grid(row=2, column=1)
    
    tk.Label(window, text="Personas kods").grid(row=3, column=0)
    personal_code_entry = tk.Entry(window)
    personal_code_entry.grid(row=3, column=1)
    
    tk.Label(window, text="Telefona numurs").grid(row=4, column=0)
    phone_number_entry = tk.Entry(window)
    phone_number_entry.grid(row=4, column=1)
    
    submit_button = tk.Button(window, text="Pievienot", command=submit)
    submit_button.grid(row=5, column=0, columnspan=2)

def find_person_window():
    def submit():
        personal_code = personal_code_entry.get()
        person = find_person_by_personal_code(personal_code)
        if person:
            person_id = person[0][0]
            info = f"Atrasta persona: {person[0][1]} {person[0][2]}, Dzimšanas gads: {person[0][3]}, Telefons: {person[0][5]}"
            person_classes = get_person_register(person_id)
            classes_info = "\n".join([f"Tips: {cls[1]}, Diena: {cls[2]}, Laiks: {cls[3]}" for cls in person_classes])
            result_text.set(info + "\n" + classes_info)
        else:
            result_text.set("Persona ar norādīto personas kodu netika atrasta")
    
    window = tk.Toplevel()
    window.title("Atrast cilvēku")
    
    tk.Label(window, text="Personas kods").grid(row=0, column=0)
    personal_code_entry = tk.Entry(window)
    personal_code_entry.grid(row=0, column=1)
    
    submit_button = tk.Button(window, text="Meklēt", command=submit)
    submit_button.grid(row=1, column=0, columnspan=2)
    
    result_text = tk.StringVar()
    result_label = tk.Label(window, textvariable=result_text)
    result_label.grid(row=2, column=0, columnspan=2)

def register_for_class_window():
    def submit():
        personal_code = personal_code_entry.get()
        person = find_person_by_personal_code(personal_code)
        if person:
            person_id = person[0][0]
            class_type = class_type_combo.get()
            class_day = class_day_combo.get()
            class_time = class_time_combo.get()
            register_for_person(person_id, class_type, class_day, class_time)
            messagebox.showinfo("Pieraksts", f"Pacients ar personas kodu {personal_code} pierakstīts uz apmeklējumu: {class_type} {class_day} {class_time}")
        else:
            messagebox.showerror("Kļūda", "Persona ar norādīto personas kodu netika atrasta")
    
    window = tk.Toplevel()
    window.title("Pieraksts uz apmeklējumu")
    
    tk.Label(window, text="Personas kods").grid(row=0, column=0)
    personal_code_entry = tk.Entry(window)
    personal_code_entry.grid(row=0, column=1)
    
    tk.Label(window, text="Apmeklējuma tips").grid(row=1, column=0)
    class_type_combo = ttk.Combobox(window, values=["Konsultācija", "Slimība", "Obligātā veselības pārbaude"])
    class_type_combo.grid(row=1, column=1)
    
    tk.Label(window, text="Diena").grid(row=2, column=0)
    class_day_combo = ttk.Combobox(window, values=["Pirmdiena", "Otrdiena", "Trešdiena", "Ceturdiena", "Piektdiena"])
    class_day_combo.grid(row=2, column=1)
    
    tk.Label(window, text="Laiks").grid(row=3, column=0)
    class_time_combo = ttk.Combobox(window, values=["09:00-09:30", "9:30-10:00","10:00-10:30", "10:30-11:00","11:00-11:30", "11:30-12:00"])
    class_time_combo.grid(row=3, column=1)
    
    submit_button = tk.Button(window, text="Pievienoties", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2)

# Galvenais logs
root = tk.Tk()
root.title("Pacientu pieraksts uz pieņemšanu")
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue") 

helv36 = tkFont.Font(family='Helvetica', size=24, weight=tkFont.BOLD)
helv18 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)

left_frame = Frame(root, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(root, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)


Label(left_frame, text="Doktorāts", font=helv36,fg='#665c5a').grid(row=0, column=0, padx=5, pady=5)

image = PhotoImage(file="doktorats.png")
original_image = image.subsample(3,3)  # resize image using subsample
Label(left_frame, image=original_image).grid(row=1, column=0, padx=5, pady=5)

Label(right_frame, image=image).grid(row=0,column=0, padx=5, pady=5)


btn = tk.Button(left_frame, text="Calendars",command=open_calendar)
btn.grid(row=3, column=0)


#tool_bar = Frame(left_frame, width=180, height=185)
#tool_bar.grid(row=2, column=0, padx=5, pady=5)
tk.Label(root, text="Izvēlēties darbību:", font=helv36,fg='#665c5a').grid(row=3, column=0, columnspan=2)

add_person_button = tk.Button(root, text="Pievienot cilvēku",font=helv18,fg='blue', bg='#b0adac', command=add_person_window)
add_person_button.grid(row=4, column=0, padx=10, pady=10)

find_person_button = tk.Button(root, text="Atrast cilvēku", font=helv18,fg='blue', bg='#b0adac',command=find_person_window)
find_person_button.grid(row=4, column=1, padx=10, pady=10)

register_button = tk.Button(root, text="Pieraksts uz apmeklējumu", font=helv18,fg='blue', bg='#b0adac',command=register_for_class_window)
register_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

exit_button = tk.Button(root, text="Iziet", font=helv18, command=root.quit)
exit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()


