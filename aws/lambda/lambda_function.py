import json
import base64
from covid_certificate_generator import pdf_generator

def lambda_handler(event, context):
    school_name = event['school']['school_name']
    print("school_name:", event['school']['school_name'], "END_EVENT")
    #print("EVENT:", event, "END_EVENT")
    school_pdf = pdf_generator.PDFGenerator()
    pdf = school_pdf.get_pdf_from_json_payload(event)
    return {
        "statusCode": 200,
        "school": school_name,
        "pdf": school_pdf.encode_to_text(pdf)
    }
