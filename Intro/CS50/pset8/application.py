import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from cs50 import SQL
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

# read API key from file
file = open("api_key.txt", "r")
key = file.readline()
file.close()

# set API key environmental variable
os.environ["API_KEY"] = key

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/articles")
def articles():
    """Look up articles for geo."""
    geo = request.args.get("geo")
    results = lookup(geo)
    return jsonify(results)

@app.route("/search")
def search():
    """Search for places that match query."""

    # aquire and format query
    query = request.args.get("q")
    query = query.replace(",", " ")
    query = re.sub(" +", " ", query)
    query = query.split(" ")

    # single item query
    if len(query) == 1:
        q = query[0]

        # postal code search
        rows = db.execute("""SELECT * FROM places
            WHERE postal_code LIKE :q
            GROUP BY postal_code
            ORDER BY RANDOM()
            LIMIT 10""",
            q="%"+q+"%")
        if len(rows) > 0:
            return jsonify(rows)

        # state acronym search
        if (len(q) == 2):
            rows = db.execute("""SELECT * FROM places
                WHERE admin_code1=:q
                ORDER BY RANDOM()
                LIMIT 10""",
                q=q.upper())
            if len(rows) > 0:
                return jsonify(rows)

        # state name search
        rows = db.execute("""SELECT * FROM places
            WHERE admin_name1 LIKE :q
            ORDER BY RANDOM()
            LIMIT 10""",
            q="%"+q+"%")
        if len(rows) > 0:
            return jsonify(rows)

        # city name search
        rows = db.execute("""SELECT * FROM places
            WHERE place_name LIKE :q
            GROUP BY admin_name1
            ORDER BY RANDOM()
            LIMIT 10""",
            q="%"+q+"%")
        if len(rows) > 0:
            return jsonify(rows)

    elif len(query) == 2:
        q0 = query[0]
        q1 = query[1]

        ## postal code search...

        # ...with place name
        rows = db.execute("""SELECT * FROM places
            WHERE postal_code LIKE :q0 AND place_name LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q0+"%", q1="%"+q1+"%")
        if len(rows) > 0:
            return jsonify(rows)

        rows = db.execute("""SELECT * FROM places
            WHERE postal_code LIKE :q0 AND place_name LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q1+"%", q1="%"+q0+"%")
        if len(rows) > 0:
            return jsonify(rows)

        # ...with state name
        rows = db.execute("""SELECT * FROM places
            WHERE postal_code LIKE :q0 AND admin_name1 LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q0+"%", q1="%"+q1+"%")
        if len(rows) > 0:
            return jsonify(rows)

        rows = db.execute("""SELECT * FROM places
            WHERE postal_code LIKE :q0 AND admin_name1 LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q1+"%", q1="%"+q0+"%")
        if len(rows) > 0:
            return jsonify(rows)

        # ...with state acronym
        rows = db.execute("""SELECT * FROM places
            WHERE postal_code LIKE :q0 AND admin_code1 LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q0+"%", q1="%"+q1+"%")
        if len(rows) > 0:
            return jsonify(rows)

        rows = db.execute("""SELECT * FROM places
            WHERE postal_code LIKE :q0 AND admin_code1 LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q1+"%", q1="%"+q0+"%")
        if len(rows) > 0:
            return jsonify(rows)

        ## state acronym search...

        # ...with state name
        rows = db.execute("""SELECT * FROM places
            WHERE admin_name1 LIKE :q0 AND admin_code1 LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q0+"%", q1="%"+q1+"%")
        if len(rows) > 0:
            return jsonify(rows)

        rows = db.execute("""SELECT * FROM places
            WHERE admin_name1 LIKE :q0 AND admin_code1 LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q1+"%", q1="%"+q0+"%")
        if len(rows) > 0:
            return jsonify(rows)

        # ...with place name
        rows = db.execute("""SELECT * FROM places
            WHERE admin_name1 LIKE :q0 AND place_name LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q0+"%", q1="%"+q1+"%")
        if len(rows) > 0:
            return jsonify(rows)

        rows = db.execute("""SELECT * FROM places
            WHERE admin_name1 LIKE :q0 AND place_name LIKE :q1
            ORDER BY RANDOM()
            LIMIT 10""",
            q0="%"+q1+"%", q1="%"+q0+"%")
        if len(rows) > 0:
            return jsonify(rows)

        ## single place name search (queries combined)
        rows = db.execute("""SELECT * FROM places
            WHERE place_name LIKE :q
            ORDER BY RANDOM()
            LIMIT 10""",
            q="%"+q0+" "+q1+"%")
        if len(rows) > 0:
            return jsonify(rows)

    # no results found
    return jsonify([])

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
