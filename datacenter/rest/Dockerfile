FROM python:3-slim

ADD . /code
WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENTRYPOINT ["tail", "-f"]
