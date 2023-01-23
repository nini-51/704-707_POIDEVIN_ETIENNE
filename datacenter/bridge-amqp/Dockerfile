FROM python:3-slim

LABEL maintainer="Louis Poidevin <louis.poidevin@etudiant.univ-reims.fr>"

COPY src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# COPY app /app

ENV AMQP_SERVER=localhost

CMD ["tail", "-f"]
# ENTRYPOINT ["python"]
# CMD ["/app/main.py"]
