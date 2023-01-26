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
            pkg['status'], pkg['warehouses'], pkg['deliver_id'], pkg['last_location'], pkg['package_id']
        )
        db.commit()
    except db.DatabaseError as e:
        error = e

    return error

###
def dict_factory(pkg):
    d = {}
    for key in pkg.keys():
        if key == 'warehouses':
            d[key] = json.loads(pkg[key])
        else:
            d[key] = pkg[key]
    return d

@api.get('/packages')
def packages():
    db = get_db()
    res = db.execute("SELECT * FROM packages").fetchall()

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
            (pkg['package_id'].upper(), pkg['status'], json.dumps(pkg['warehouses']), pkg['deliver_id'], pkg['last_location'])
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
    db = get_db()
    try:
        db.execute("""
            INSERT INTO archives (package_id, status, warehouses, deliver_id, last_location)
            SELECT package_id, status, warehouses, deliver_id, last_location
            FROM packages;
            WHERE package_id = ?
            """, package_id.upper()
        )
        db.execute(
            "DELETE FROM packages WHERE package_id = ?", package_id.upper()
        )
        db.commit()
    except Error as error:
        abort(500, error)
    return jsonify(package_id.upper()), 204
