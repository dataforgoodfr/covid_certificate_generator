import streamlit as st
from io import StringIO,BytesIO
from covid_certificate_generator import core
import os, sys
import base64
import datetime


# https://alexanderankin.github.io/pyfpdf/mkdocs_docs/FAQ/index.html

# LAYOUT
# https://docs.streamlit.io/en/stable/api.html#lay-out-your-app
# https://discuss.streamlit.io/t/amend-streamlits-default-colourway-like-on-the-spacy-streamlit-app/4184/10

st.set_page_config(
    page_title="Générateur de justificatifs",
    layout="wide",
    page_icon="streamlit_app/assets/favicon-32x32.png",

)
    
with open("streamlit_app/navbar-bootstrap.html","r") as navbar:
    st.markdown(navbar.read(),unsafe_allow_html=True)




# From https://discuss.streamlit.io/t/how-to-center-images-latex-header-title-etc/1946/4
with open("streamlit_app/style.css") as f:
    st.markdown("""<link href='http://fonts.googleapis.com/css?family=Roboto:400,100,100italic,300,300italic,400italic,500,500italic,700,700italic,900italic,900' rel='stylesheet' type='text/css'>""", unsafe_allow_html=True)
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



left_column, right_column = st.beta_columns([1,2])
# You can use a column just like st.sidebar:

with left_column:
    # st.image("app/assets/science_discovery (1).png")
    st.info("Cet outil a pour but de faciliter la génération de **JUSTIFICATIFS DE DÉPLACEMENT SCOLAIRE** par les établissements scolaires à partir de la liste des élèves.")

    st.write("Générez facilement un PDF avec toutes les attestations comme montré ci-dessous")
    st.image("assets/pdf_view.png")
    st.write("#### 📧 Contact\nPour plus d'informations ou améliorer cet outil pour le rendre plus utile, contactez [Benoit Courty](http://courty.fr/#contact_section) par mail")
    st.write("#### 🌎 Data For Good\nCet outil est construit à 100% par des bénévoles au sein de l'association [Data For Good](https://dataforgood.fr)")

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    st.write("## Générateur de justificatifs dérogatoire de déplacement scolaire")
    st.write("**1. Pré-requis** : préparez un fichier excel avec les informations des élèves suivantes (respectez bien le nom des colonnes)")
    st.image("assets/excel.png")
    st.write("**2. Remplissez à présent le formulaire suivant** pour ajouter les informations de l'établissement")


    students_file = st.file_uploader("Fichier excel ou csv avec la liste des élèves inscrite comme ci-dessus",type=["xls","csv","xlsx"])
    school_name = st.text_input("Nom de l'établissement scolaire")
    school_address = st.text_input("Addresse de l'établissement scolaire")
    school_city = st.text_input("Ville de signature")
    school_sign = st.file_uploader("Cachet de l'établissement",type=["png","jpg","jpeg"])

    st.write("**3. Générez le PDF** avec les justificatifs à imprimer en cliquant ci-dessous")



    if school_sign is not None and students_file is not None:
        school_sign.seek(0)

        school_pdf_str = None

        run_pdf = st.button("Générer le PDF")
        if run_pdf:

            school={
                'school_name':school_name,
                'school_adress':school_address,
                'school_sign':school_sign,
                'city':school_city
            }

            school_pdf = core.PDFGenerator(students_file, school)
            school_pdf_str = base64.b64encode(school_pdf.get_pdf("test.pdf",return_object = True))

            today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            if school_pdf_str is not None:
                st.markdown(f'<a download="Justificatifs_{today}.pdf" target="_blank" href="data:application/pdf;base64,{school_pdf_str.decode()}"><b>Télécharger le fichier en cliquant ici !</a>',unsafe_allow_html = True)



    else:
        st.warning("Le formulaire doit être rempli entièrement avant de pouvoir générer le Fichier")

# import PySimpleGUI as sg
# from covid_certificate_generator import core
# import os, sys

# file_list_column = [
#     [
#         sg.Text("Cachet de l'établissement"),
#         sg.In(size=(25, 1), enable_events=True, key="-CACHET-"),
#         sg.FileBrowse()
#     ],
#     [
#         sg.Text("Fichier des élèves"),
#         sg.In(size=(25, 1), enable_events=True, key="-STUDENTS-"),
#         sg.FileBrowse() # file_types=(("Image", "*.jpg"),)
#     ],
#     [sg.Text('Etablissement :')],
#     [sg.Text('Nom', size=(15, 1)), sg.InputText('Ecole Jean Jaurès', key='-NAME-')],
#     [sg.Text('Adresse', size=(15, 1)), sg.InputText('2 rue des Ecoles à Libreville', key='-ADDRESS-')],
#     [sg.Text('Ville de signature', size=(15, 1)), sg.InputText('Libreville', key='-CITY-')],
# ]

# image_viewer_column = [

#     [sg.InputText('rien', visible=False, enable_events=True, key='file_path'),
#     sg.FileSaveAs(file_types=(('PDF', '.pdf'),))],
    
#     [sg.Text("Choose an image from list on left:", visible=False, key="-LOG-")],
#     [sg.Text(size=(40, 1), key="-TOUT-")],
#     [sg.Image(key="-IMAGE-")],
#     [sg.Button("Quitter")],
# ]

# # ----- layout -----
# layout = [
#     [
#         sg.Column(file_list_column),
#         sg.VSeperator(),
#         sg.Column(image_viewer_column),
#     ]
# ]

# window = sg.Window("Générateur d'attestation", layout)
# cachet = None
# students_file = None
# while True:
#     event, values = window.read()
#     print("event", event)
#     if event == "Quitter" or event == sg.WIN_CLOSED:
#         break
#     if event == "-STUDENTS-":
#         students_file = values["-STUDENTS-"]
#     # Folder name was filled in, make a list of files in the folder
#     if event == "-CACHET-":
#         cachet = values["-CACHET-"]
#         print("cachet", cachet)
#         try:
#             window["-IMAGE-"].update(filename=cachet)
#         except:
#             print("Error reading :", cachet)
#             pass
#     elif event == "file_path":
#         window["-TOUT-"].update("Génération en cours...")
#         output_file = values['file_path']
#         try:
#             school={
#                 'school_name':values["-NAME-"],
#                 'school_adress':values["-ADDRESS-"],
#                 'school_sign':cachet,
#                 'city':values["-CITY-"]
#             }
#             school_pdf = core.PDFGenerator(students_file, school)
#             school_pdf.get_pdf(output_file)
#             window["-TOUT-"].update("Génération terminée !")
#         except:
#             error = f'ERREUR : {sys.exc_info()[0]}'
#             window["-TOUT-"].update(error)
#             print(error)

# window.close()