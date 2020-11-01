FROM python:3.7.0

RUN apt-get update && apt-get upgrade -y && /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir -p /opt/covid_certificate_generator/logs
WORKDIR /opt/covid_certificate_generator/
COPY requirements.txt .
COPY index.py .
COPY streamlit_app ./streamlit_app
COPY covid_certificate_generator ./covid_certificate_generator
COPY assets ./assets


EXPOSE 8501

RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /opt/covid_certificate_generator
CMD [ "streamlit", "run", "index.py"]
