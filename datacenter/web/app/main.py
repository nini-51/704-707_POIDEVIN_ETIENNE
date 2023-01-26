from flask import Flask, request, jsonify, json
from werkzeug.exceptions import abort
# from flask_cors import CORS

from app.db import init_app, get_db

api = Flask(__name__)
web.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY = "dev",
    # path of the database
    DATABASE = "/var/lib/sqlite/delivery.sqlite"
)
# CORS(app, resources={r"/*": {"origins": "*"}})

# register the database commands
init_app(web)


@web.route('/')
def update_package(package_id):
    """
    Update a package
    """
    return "soon"

@web.route('/suivre_mon_colis')
def update_package(package_id):
    """

    """
    db = get_db()

    cur = con.cursor()
    cur.execute("SELECT * FROM packages WHERE package_id = ")

    packages = cur.fetchall();
    return "soon"

@web.route('/<int:package_id>/')
def package(package_id):
    package = package.query.get_or_404(package_id)
    return render_template('package.html', package=package)

@web.route('/liste')
def liste(package_id):
    """
    Update a package
    """
    db = get_db()

    cur = con.cursor()
    cur.execute("SELECT * FROM packages")

    packages = cur.fetchall();
    return render_template("liste.html", packages = packages)



@web.route('/suivre_mon_colis/<string:package_id>')
def update_package(package_id):
    """
    Update a package
    """
    return "soon"



# # compose_flask/app.py
# from flask import Flask, request, jsonify
# import json
# import sqlite3
# # from flask_cors import CORS
#
#
# web = Flask(__name__)
# # CORS(app, resources={r"/*": {"origins": "*"}})
#
#
#
# def connect_db_connection():
#     conn = sqlite3.connect('database.db')
#     return conn
#
# def get_objects():
#     users = []
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM objects")
#         rows = cur.fetchall()
#
#         # convert row objects to dictionary
#         for i in rows:
#             object = {}
#             object["object_id"] = i["object_id"]
#             object["status"] = i["status"]
#             object["warehouse_id"] = i["warehouse_id"]
#             object["deliver_id"] = i["deliver_id"]
#             object["time"] = i["time"]
#             object["gps"] = i["gps"]
#             objects.append(object)
#
#     except:
#         objects = []
#
#     return objects
#
#
# def get_object_by_id(object_id):
#     object = {}
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM objects WHERE object_id = ?",
#                        (object_id,))
#         row = cur.fetchone()
#
#         # convert row object to dictionary
#         object["object_id"] = row["object_id"]
#         object["status"] = row["status"]
#         object["warehouse_id"] = row["warehouse_id"]
#         object["deliver_id"] = row["deliver_id"]
#         object["time"] = row["time"]
#         object["gps"] = row["gps"]
#     except:
#         object = {}
#
#     return object
#
#
# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>VLib - Online Library</h1><p>A flask api implementation for book information.   </p>'''
#
#
# @app.route('/api/objects', methods=['GET'])
# def api_get_objects():
#     return jsonify(get_objects())
#
# @app.route('/api/objects/<object_id>', methods=['GET'])
# def api_get_object(object_id):
#     return jsonify(get_object_by_id(object_id))
#
#
# if __name__ == "__main__":
#     #app.debug = True
#     #app.run(debug=True)
#     web.run() #run app
