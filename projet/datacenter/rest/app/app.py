# compose_flask/app.py
from flask import Flask
from redis import Redis
import json
import mariadb

app = Flask(__name__)

conn = mariadb.connect(
         host='db',
         port= 8080,
         user='user',
         password='user',
         database='colis')
cur = conn.cursor()


@app.route('/index')
def index():
    return "Connected to database"


@app.route('/objects', POST)
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')
def index():
    #connexion for mariadb
    conn= mariadb.connect(**config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
