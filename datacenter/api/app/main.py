from flask import Flask, request, jsonify
# from flask_cors import CORS
import json

from app.db import init_db, get_db

api = Flask(__name__)
api.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY = "dev",
    # path of the database
    DATABASE = "/var/lib/sqlite/delivery.sqlite"
)
# CORS(app, resources={r"/*": {"origins": "*"}})

# init the database
with api.app_context():
    init_db()

def new_package(package):
    db = get_db()
    error = None

    try:
        db.execute(
            "INSERT INTO packages (package_id, status, warehouse_id, deliver_id, time, gps) VALUES (?,?,?,?,?,?)",
            (package['package_id'], package['status'], package['warehouse_id'], package['deliver_id'], package['time'], package['gps']),
        )
        db.commit()
    except db.IntegrityError:
        print(f"Package {package['package_id']} is already registered.")
    # return
    # return inserted_package

def update_package(package):
    db = get_db()
    error = None

    try:
        db.execute(
            "UPDATE packages SET status = ?, warehouse_id = ?, deliver_id = ?, time = ?, gps = ? WHERE package_id =?",
            status['status'], warehouse_id['warehouse_id'], deliver_id['deliver_id'], time['time'], gps['gps'],
        )
        db.commit()
    except db.DatabaseError as error:
        print(f"error: {e}")
    # return
    # return updated_user

@api.route('/', methods=['GET'])
def home():
    return '''<h1>VLib - Online Library</h1><p>A flask api implementation for book information.   </p>'''

@api.route('/api/users/add',  methods = ['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@api.route('/api/users/update',  methods = ['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

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
#     @api.route('/index')
#     def hello():
#         return 'Hello, World!'
#
#     return app
