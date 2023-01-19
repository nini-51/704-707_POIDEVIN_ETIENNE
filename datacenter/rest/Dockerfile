FROM python
ADD . /code
WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["tail", "-f"]
