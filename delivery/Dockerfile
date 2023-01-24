FROM python:3-slim

LABEL maintainer="Louis Poidevin <louis.poidevin@etudiant.univ-reims.fr>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app /app

ENV AMQP_SERVER="localhost"

ENTRYPOINT ["python", "/app/main.py"]
CMD ["DEMO"]
