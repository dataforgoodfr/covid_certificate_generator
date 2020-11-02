import streamlit as st
from io import StringIO,BytesIO
from covid_certificate_generator import pdf_generator
import os, sys
import base64
import datetime
import requests
import json

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
    st.write("Note RGPD : Vous devez avoir obtenu le consentement des personnes pour ce traitement. Les informations vont transiter sur internet de façon sécurisée (https) et le fichier des élèves ne sera pas stocké.")
    st.write("**2. Remplissez à présent le formulaire suivant** pour ajouter les informations de l'établissement")

    students_file = st.file_uploader("Fichier excel ou csv avec la liste des élèves inscrite comme ci-dessus",type=["xls","csv","xlsx"])
    school_name = st.text_input("Nom de l'établissement scolaire")
    school_address = st.text_input("Adresse de l'établissement scolaire")
    school_city = st.text_input("Ville de signature")
    school_sign = st.file_uploader("Cachet de l'établissement",type=["png","jpg","jpeg"])

    st.write("**3. Générez le PDF** avec les justificatifs à imprimer en cliquant ci-dessous")



    if school_sign is not None and students_file is not None:
        school_sign.seek(0)
        students_file.seek(0)

        school_pdf_str = None
        school_pdf = pdf_generator.PDFGenerator()
        run_pdf = st.button("Générer le PDF")
        if run_pdf:

            school={
                'school_name':school_name,
                'school_adress':school_address,
                #'school_sign':base64.b64encode(school_sign.read()),
                'city':school_city
            }
            data = {
                'students_file' : school_pdf.encode_to_text(students_file.read()),
                'school_sign' : school_pdf.encode_to_text(school_sign.read()),
                'school': school
            }
            url = 'https://xa1scavw1l.execute-api.eu-west-3.amazonaws.com/test/pdf'
            
            #print("\n\n", json.dumps(data), "\n\n")
            #print(f'Calling {url}')
            response = requests.post(url, data=json.dumps(data))
            if response.status_code != 200:
                st.error(f"Erreur lors de la génération du PDF. Code retour : {response.status_code}")
            else:
                #print(response)
                response_data = response.json()
                #print(response_data)
                # school_pdf = pdf_generator.PDFGenerator()
                # #print(type(students_file))
                # school_pdf_str = base64.b64encode(
                #     school_pdf.get_pdf_from_file(students_file, school_sign, school, output_name=school_pdf.get_temp_file(), return_object = True)
                # )
                pdf = response_data["pdf"]
                today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                if len(pdf) > 100:
                    st.markdown(f'<a download="Justificatifs_{today}.pdf" target="_blank" href="data:application/pdf;base64,{pdf}"><b>Télécharger le fichier en cliquant ici !</a>',unsafe_allow_html = True)
                else:
                    st.error("Erreur lors de la génération du PDF.")

    else:
        st.warning("Le formulaire doit être rempli entièrement avant de pouvoir générer le fichier")