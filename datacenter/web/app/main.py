from flask import Flask, request, jsonify, json
from werkzeug.exceptions import abort
# from flask_cors import CORS

from app.db import init_app, get_db

app = Flask(__name__)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY = "dev",
    # path of the database
    DATABASE = "/var/lib/sqlite/delivery.sqlite"
)
# CORS(app, resources={r"/*": {"origins": "*"}})

# register the database commands
init_app(app)


@app.route('/')
def update_package(package_id):
    """
    Home page; redirect to find package page
    """
    return redirect(url_for('/find_my_package'))

@app.route('/find_my_package')
def update_package(package_id):
    """
    Page to find a package with exact package id
    """
    db = get_db()
    search = request.args.get('search')

    if search:
        try:
            package = db.execute("SELECT * FROM packages WHERE package_id = ?", (search.upper())).fetchone()
        except db.DatabaseError as error:
            abord(400, error)

    return render_template('search.html', package = package)


@app.route('/list')
def list(package_id):
    """
    Update a package
    """
    db = get_db()

    cur = con.cursor()
    cur.execute("SELECT * FROM packages")
    packages = cur.fetchall();

    return render_template("list.html", packages = packages)
