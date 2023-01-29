from flask import Flask, request, redirect, flash, render_template, url_for, json
from werkzeug.exceptions import abort

from app.db import init_app, get_db

web = Flask(__name__)
web.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY = "dev",
    # path of the database
    DATABASE = "/var/lib/sqlite/delivery.sqlite"
)

# init the database
with web.app_context():
    init_app()

def dict_factory(pkg):
    d = {}
    for key in pkg.keys():
        if key == 'warehouses':
            d[key] = json.loads(pkg[key])
        elif key == 'last_location':
            d[key] = json.loads(pkg[key])
        else:
            d[key] = pkg[key]
    return d

@web.route('/')
def home():
    """
    Home page; redirect to find package page
    """
    return redirect(url_for('track_package'))

@web.route('/track-a-parcel')
def track_package():
    """
    Page to find a package with exact package id
    """
    db = get_db()
    search = request.args.get('search')
    package = []

    if search:
        try:
            res = db.execute("SELECT * FROM packages WHERE package_id = ?", (search.upper(),)).fetchone()
        except db.DatabaseError as error:
            flash(f"Error: {error}")

    if search:
        if not res:
            flash(f"Parcel number {search} does not exist.")
        else:
            package = dict_factory(res)

    return render_template('search.html', package = package)

@web.route('/list')
def list_package():
    """
    List all parcels
    """
    db = get_db()
    try:
        res = db.execute("SELECT * FROM packages").fetchall()
    except db.DatabaseError as error:
        flash(f"Error: {error}")

    packages = list(map(lambda package : dict_factory(package), res))

    return render_template("list.html", packages = packages)
