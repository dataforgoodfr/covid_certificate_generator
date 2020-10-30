import PySimpleGUI as sg
from covid_certificate_generator import core
import os

# First the window layout in 2 columns


file_list_column = [
    [
        sg.Text("Cachet de l'établissement"),
        sg.In(size=(25, 1), enable_events=True, key="-CACHET-"),
        #sg.FolderBrowse(),
        sg.FileBrowse() # file_types=(("Image", "*.jpg"),)
    ],
    [
        sg.Text("Fichier des élèves"),
        sg.In(size=(25, 1), enable_events=True, key="-STUDENTS-"),
        #sg.FolderBrowse(),
        sg.FileBrowse() # file_types=(("Image", "*.jpg"),)
    ],
    [sg.Text('Etablissement :')],
    [sg.Text('Nom', size=(15, 1)), sg.InputText('Ecole Jean Jaurès', key='-NAME-')],
    [sg.Text('Address', size=(15, 1)), sg.InputText('2 rue des Ecoles à Libreville', key='-ADDRESS-')],
    [sg.Text('Ville', size=(15, 1)), sg.InputText('Libreville', key='-CITY-')],
]

# For now will only show the name of the file that was chosen

image_viewer_column = [
    #[sg.Button("Generer")],
    #sg.InputText(key='Generer', do_not_clear=False, enable_events=True, visible=False),
    #[sg.FileSaveAs(key='Generer', initial_folder='./')],
    #
    [sg.InputText('rien', visible=False, enable_events=True, key='file_path'),
    sg.FileSaveAs(file_types=(('PDF', '.pdf'),))],
    [sg.Button("Quitter")],
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Generateur d'attestation", layout)
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
        #window["-FILE LIST-"].update(fnames)
        # print("file_list", file_list)
    # elif event == "-FILE LIST-":  # A file was chosen from the listbox
    #     #try:
    #         filename = os.path.join(
    #             values["-FOLDER-"], values["-FILE LIST-"][0]
    #         )
    #         window["-TOUT-"].update(filename)
    #         window["-IMAGE-"].update(filename=filename)
    #         print(filename)
    #     #except:
    #     #    pass
    elif event == "file_path":
        output_file = values['file_path']
        try:
            school={
                'school_name':values["-NAME-"],
                'school_adress':values["-ADDRESS-"],
                'school_sign':cachet,
                'city':values["-CITY-"]
            }
            #students_file = 'data.csv'
            school_pdf = core.PDFGenerator(students_file, school)
            school_pdf.get_pdf(output_file)
            print("Genéré")
        except:
            print("ERROR", output_file)

# layout = [[sg.Text("Hello from PySimpleGUI")],
#     [sg.Button("Generer")],
#     [sg.Button("Quitter")]]

# # Create the window
# window = sg.Window("Generateur d'attestation", layout)

# # Create an event loop
# while True:
#     event, values = window.read()
#     if event == "Generer":
#         school={
#             'school_name':'Ecole Jean Jaurès',
#             'school_adress':'rue Jean Jaurès, 42 000 Libreville',
#             'school_sign':'cachet.jpg',
#             'city':'Libreville'
#         }
#         students_file = 'data.csv'
#         school_pdf = core.PDFGenerator(students_file, school)
#         school_pdf.get_pdf('test.pdf')
#     # End program if user closes window or
#     # presses the OK button
#     if event == "Quitter" or event == sg.WIN_CLOSED:
#         break

# window.close()