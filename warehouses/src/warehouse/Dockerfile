FROM python:3-slim

LABEL maintainer="Louis Poidevin <louis.poidevin@etudiant.univ-reims.fr>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app

ENV WAREHOUSE_ID="DEMO"
ENV API_SERVER="localhost"

ENTRYPOINT ["python3"]
CMD ["/app/main.py"]
