import PySimpleGUI as sg
from covid_certificate_generator import core
import os, sys

file_list_column = [
    [
        sg.Text("Cachet de l'établissement"),
        sg.In(size=(25, 1), enable_events=True, key="-CACHET-"),
        sg.FileBrowse()
    ],
    [
        sg.Text("Fichier des élèves"),
        sg.In(size=(25, 1), enable_events=True, key="-STUDENTS-"),
        sg.FileBrowse() # file_types=(("Image", "*.jpg"),)
    ],
    [sg.Text('Etablissement :')],
    [sg.Text('Nom', size=(15, 1)), sg.InputText('Ecole Jean Jaurès', key='-NAME-')],
    [sg.Text('Adresse', size=(15, 1)), sg.InputText('2 rue des Ecoles à Libreville', key='-ADDRESS-')],
    [sg.Text('Ville de signature', size=(15, 1)), sg.InputText('Libreville', key='-CITY-')],
]

image_viewer_column = [

    [sg.InputText('rien', visible=False, enable_events=True, key='file_path'),
    sg.FileSaveAs(file_types=(('PDF', '.pdf'),))],
    
    [sg.Text("Choose an image from list on left:", visible=False, key="-LOG-")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("Quitter")],
]

# ----- layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Générateur d'attestation", layout)
cachet = None
students_file = None
while True:
    event, values = window.read()
    print("event", event)
    if event == "Quitter" or event == sg.WIN_CLOSED:
        break
    if event == "-STUDENTS-":
        students_file = values["-STUDENTS-"]
    # Folder name was filled in, make a list of files in the folder
    if event == "-CACHET-":
        cachet = values["-CACHET-"]
        print("cachet", cachet)
        try:
            window["-IMAGE-"].update(filename=cachet)
        except:
            print("Error reading :", cachet)
            pass
    elif event == "file_path":
        window["-TOUT-"].update("Génération en cours...")
        output_file = values['file_path']
        try:
            school={
                'school_name':values["-NAME-"],
                'school_adress':values["-ADDRESS-"],
                'school_sign':cachet,
                'city':values["-CITY-"]
            }
            school_pdf = core.PDFGenerator(students_file, school)
            school_pdf.get_pdf(output_file)
            window["-TOUT-"].update("Génération terminée !")
        except:
            error = f'ERREUR : {sys.exc_info()[0]}'
            window["-TOUT-"].update(error)
            print(error)

window.close()