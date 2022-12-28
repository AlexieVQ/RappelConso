FROM python:3.11
WORKDIR /usr/src/rappelconso
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./rappelconso .
RUN mkdir /var/rappelconso
VOLUME [ "/var/rappelconso" ]
ENV RAPPELCONSO_FICHIER_HISTORIQUE=/var/rappelconso/historique.txt
CMD ["python", "main.py"]
