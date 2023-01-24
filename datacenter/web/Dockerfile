FROM python:3-slim

LABEL maintainer="Louis Poidevin <louis.poidevin@etudiant.univ-reims.fr>"

COPY requirements.txt /tmp/requirements.txt
COPY gunicorn-conf.py /gunicorn-conf.py

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# COPY app /app

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0"
EXPOSE 8000

ENTRYPOINT ["gunicorn", "--config", "/gunicorn-conf.py"]
CMD ["app.main:web"]
