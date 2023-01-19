# compose_flask/app.py
from flask import Flask, request, jsonify
# from flask_cors import CORS
import json
import sqlite3

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})


def connect_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            DROP TABLE IF EXISTS objects;

            CREATE TABLE objects (
              object_id INTEGER PRIMARY KEY NOT NULL,
              status TEXT NOT NULL,
              warehouse_id INTEGER NOT NULL,
              deliver_id INTEGER NOT NULL,
              time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              gps TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("objects table created successfully")
    except:
        print("objects table creation failed - Maybe table")
    finally:
        conn.close()

def insert_object(object):
    inserted_object = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO objects (object_id, status, warehouse_id, deliver_id, time, gps) VALUES (?,?,?,?,?,?)", (object_id['object_id'], status['status'], warehouse_id['warehouse_id'], deliver_id['deliver_id'], time['time'], gps['gps']))
        conn.commit()
        # insert_object = get_object_by_id(cur.lastrowid)
    except:
        conn().rollback()
    finally:
        conn.close()
    return
    # return inserted_object

def update_object(object):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE objects SET status = ?, warehouse_id = ?, deliver_id = ?, time = ?, gps = ? WHERE object_id =?", status['status'], warehouse_id['warehouse_id'], deliver_id['deliver_id'], time['time'], gps['gps'])
        conn.commit()
        #return the user
        # updated_user = get_user_by_id(user["user_id"])

    except:
        conn.rollback()
        updated_object = {}
    finally:
        conn.close()
    return
    # return updated_user

@app.route('/', methods=['GET'])
def home():
    return '''<h1>VLib - Online Library</h1><p>A flask api implementation for book information.   </p>'''

@app.route('/api/users/add',  methods = ['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/update',  methods = ['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.run() #run app

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='user',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#     )
#
#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)
#
#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
#
#     # a simple page that says hello
#     @app.route('/index')
#     def hello():
#         return 'Hello, World!'
#
#     return app
