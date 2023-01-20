FROM python:3-slim

LABEL maintainer="Louis Poidevin <louis.poidevin@etudiant.univ-reims.fr>"

WORKDIR /srv

COPY ./requirements.txt /srv/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app/main.py"]
