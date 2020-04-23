FROM python:3.8.1-alpine

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY app.py .
COPY templates templates

# Copy the version number into the container
COPY VERSION.txt .

EXPOSE 5000

ENV FLASK_APP app.py

CMD [ "flask", "run", "--host=0.0.0.0" ]