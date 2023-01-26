from flask import Flask, request, jsonify, json
from werkzeug.exceptions import abort
# from flask_cors import CORS

from app.db import init_app, get_db

api = Flask(__name__)
api.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY = "dev",
    # path of the database
    DATABASE = "/var/lib/sqlite/delivery.sqlite"
)
# CORS(app, resources={r"/*": {"origins": "*"}})

# register the database commands
init_app(api)

def update_entry(pkg):
    db = get_db()
    error = None

    try:
        db.execute(
            "UPDATE packages SET status = ?, warehouses = ?, deliver_id = ?, last_location = ? WHERE package_id = ?",
            pkg['status'], pkg['warehouses'], pkg['deliver_id'], pkg['last_location'], pkg['package_id'],
        )
        db.commit()
    except db.DatabaseError as e:
        error = e

    return error

###
@api.get('/packages')
def packages():
    db = get_db()
    res = db.execute("SELECT * FROM packages").fetchall()
    def dict_factory(pkg):
        d = {}
        for key in pkg.keys():
            if key == 'warehouses':
                d[key] = json.loads(pkg[key])
            else:
                d[key] = pkg[key]
        return d
    packages = list(map(lambda package : dict_factory(package), res))
    return jsonify(packages)

@api.post('/packages')
def new_package():
    """
    Register a new package
    """
    try:
        payload = request.get_json()
    except json.decoder.JSONDecodeError as error:
        abort(400, error)

    if payload['status'] != 'in transit':
        abort(400, "Invalid status for registration")

    pkg = {
        'package_id': payload['package_id'],
        'status': payload['status'],
        'warehouses': [ (payload['warehouse_id'], payload['timestamp']) ],
        'deliver_id': None,
        'last_location': payload['warehouse_id']
    }

    db = get_db()
    try:
        db.execute(
            "INSERT INTO packages (package_id, status, warehouses, deliver_id, last_location) VALUES (?,?,?,?,?)",
            (pkg['package_id'], pkg['status'], json.dumps(pkg['warehouses']), pkg['deliver_id'], pkg['last_location']),
        )
        db.commit()
    except db.IntegrityError:
        abort(400, f"Package {pkg['package_id']} is already registered.")

    return jsonify(pkg['package_id']), 201


@api.put('/packages/<string:package_id>')
def update_package(package_id):
    """
    Update a package
    """
    return "soon"


@api.delete('/packages/<string:package_id>')
def delete_package(package_id):
    """
    Move a package into archives
    """
    return "soon"

# @api.route('/api/users/add',  methods = ['POST'])
# def api_add_user():
#     user = request.get_json()
#     return jsonify(insert_user(user))
#
# @api.route('/api/users/update',  methods = ['PUT'])
# def api_update_user():
#     user = request.get_json()
#     return jsonify(update_user(user))

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
