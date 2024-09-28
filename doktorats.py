import sqlite3
import PySimpleGUI as sg

def execute_query(query, parameters=()):
    conn = sqlite3.connect('sportisti.db')
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

def add_person_to_database(first_name, last_name, birth_year, personal_code, phone_number):
    query = 'INSERT INTO people (first_name, last_name, birth_year, personal_code, phone_number) VALUES (?, ?, ?, ?, ?)'
    execute_query(query, (first_name, last_name, birth_year, personal_code, phone_number))

def find_person_by_personal_code(personal_code):
    query = 'SELECT * FROM people WHERE personal_code=?'
    return execute_query(query, (personal_code,))

def register_for_class(person_id, class_type, class_day, class_time):
    query = 'INSERT INTO class_registration (person_id, class_type, class_day, class_time) VALUES (?, ?, ?, ?)'
    execute_query(query, (person_id, class_type, class_day, class_time))

def get_person_classes(person_id):
    query = 'SELECT id, class_type, class_day, class_time FROM class_registration WHERE person_id = ?'
    return execute_query(query, (person_id,))

def delete_class_registration(person_id, registration_id):
    print('dsdsdsds', person_id, registration_id)
    query = 'DELETE FROM class_registration WHERE person_id = ? AND id = ?'
    execute_query(query, (person_id, registration_id,))
    

# loga makets
layout = [
    [sg.Text('Izvelēties darbību:')],
    [sg.Radio('Pievienot cilvēku', "RADIO1", default=True, key='add_radio'), sg.Radio('Atrast cilveku ar personas kodu', "RADIO1", key='find_radio')],
    [sg.Text('Vards'), sg.InputText(key='first_name')],
    [sg.Text('Uzvards'), sg.InputText(key='last_name')],
    [sg.Text('Dzimšanas gads'), sg.InputText(key='birth_year')],
    [sg.Text('Personas kods'), sg.InputText(key='personal_code')],
    [sg.Text('Telefona numurs'), sg.InputText(key='phone_number')],
    [sg.Button('Izpildīt'), sg.Button('Pieraksts'), sg.Button('Iziet')],
    [sg.Text(size=(40, 1), key='output')]
]

# Logs
window = sg.Window('Datubāzes vadība').Layout(layout)

# Darbība ar logu
while True:
    event, values = window.Read()
    if event is None or event == 'Iziet':
        break
    if event == 'Izpildīt':
        if values['add_radio']:
            add_person_to_database(values['first_name'], values['last_name'], values['birth_year'], values['personal_code'], values['phone_number'])
            window['output'].update('Persona pievienota datu bāzei')
        elif values['find_radio']:
            person = find_person_by_personal_code(values['personal_code'])
            if person:
                person_id = person[0][0]
                person_classes = get_person_classes(person_id)
                info_layout = [
                    [sg.Text('Personas info')],
                    [sg.Text(f"Atrasta persona: {person[0][1]} {person[0][2]}, Dzimšanas gads: {person[0][3]}, Telefons: {person[0][5]}")],
                    [sg.Text('Personas nodarbības:')],
                ]
                for class_info in person_classes:
                    info_layout.append([sg.Text(f"Tips: {class_info[0]}, Diena: {class_info[1]}, Laiks: {class_info[2]}")])
                info_layout.append([sg.Button('Aizvert')])
                info_window = sg.Window('Personas info').Layout(info_layout)
                info_event, info_values = info_window.Read()
                if info_event == 'Aizvert' or info_event is None:
                    info_window.close()
            else:
                window['output'].update('Cilvēks ar tādu personas kodu nav atrasts.')
    elif event == 'Pieraksts':
        register_layout = [
            [sg.Text('Personas kods'), sg.InputText(key='personal_code')],
            [sg.Text('Izveleties slimības iemeslu:'), sg.Combo(['Konsultācija', 'Slimība'], key='class_type')],
            [sg.Text('Izveleties dienu:'), sg.Combo(['Pirmdiena', 'Otrdiena', 'Trešdiena', 'Ceturdiena', 'Piektdiena'], key='class_day')],
            [sg.Text('Izveleties laiku:'), sg.Combo(['09:00-09:30', '9:30-10:00'], key='class_time')],
            [sg.Button('Pievienoties'), sg.Button('Dzēst ierakstu'), sg.Button('Iziet')],
            [sg.Text(size=(40, 1), key='output')]
        ]
        register_window = sg.Window('Reģistrācija uz nodarbību').Layout(register_layout)

        while True:
            event, values = register_window.Read()
            if event is None or event == 'Iziet':
                register_window.close()
                break
            elif event == 'Pievienoties':
                person = find_person_by_personal_code(values['personal_code'])
                if person:
                    person_id = person[0][0]
                    class_type = values['class_type']
                    class_day = values['class_day']
                    class_time = values['class_time']
                    register_for_class(person_id, class_type, class_day, class_time)
                    register_window['output'].update(f'Cilvēks pierakstīts uz nodarbību {class_type}  {class_day}  {class_time}')
                else:
                    register_window['output'].update('Persona ar norādīto personas kodu netika atrasta')
            elif event == 'Dzēst ierakstu':
                person = find_person_by_personal_code(values['personal_code'])
                if person:
                    person_id = person[0][0]
                    person_classes = get_person_classes(person_id)
                    delete_layout = [
                        [sg.Text('Izveleties pierakstu kuru dzēst:')],
                    ]
                    for class_info in person_classes:
                        class_info_with_id = list(class_info)  
                        class_info_with_id.append(class_info[0]) 
                        delete_layout.append([sg.Radio(f"Tips: {class_info[0]}, Diena: {class_info[1]}, Laiks: {class_info[2]}", group_id='class_to_delete', key=class_info_with_id[3])])
                    delete_layout.append([sg.Button('Dzēst')])
                    delete_window = sg.Window('Pierakstu dzēšana').Layout(delete_layout)
                    delete_event, delete_values = delete_window.Read()
                    print('gdgdf',class_info[0])
                    if delete_event == 'Dzēst':
                        for class_info in person_classes:
                            if delete_values[class_info[0]]:
                                delete_class_registration(person_id, class_info[0])  
                                #delete_class_registration(person_id, class_info[0]) 
                                register_window['output'].update(f'Pieraksts uz {class_info[0]} ir dzēsta')
                                break
                    delete_window.close()
window.close()
