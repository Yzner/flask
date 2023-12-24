#leagues
from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

leagues_app = Blueprint('leagues', __name__)

# Configure MySQL
mysql = MySQL()

# Define your routes under the players blueprint
# @players_app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@leagues_app.route("/leagues", methods=["GET"])
def get_leagues():
    data = data_fetch("""SELECT * FROM leagues""")
    return make_response(jsonify(data), 200)

@leagues_app.route("/leagues/<int:id>", methods=["GET"])
def get_league_by_id(id):
    data = data_fetch("""SELECT * FROM Leagues WHERE league_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@leagues_app.route("/leagues", methods=["POST"])
def add_league():
    cur = mysql.connection.cursor()
    info = request.get_json()
    league_id = info["league_id"]
    league_details = info["league_details"]
    league_name = info["league_name"]
    cur.execute(
        """INSERT INTO Leagues (league_id, league_details, league_name) VALUES (%s, %s, %s)""",
        (league_id, league_details, league_name),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "league added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@leagues_app.route("/leagues/<int:id>", methods=["PUT"])
def update_league(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    league_details = info["league_details"]
    league_name = info["league_name"]
    cur.execute(
        """UPDATE Leagues SET league_details = %s, league_name = %s WHERE league_id = %s""",
        (league_details, league_name, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "League updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@leagues_app.route("/leagues/<int:id>", methods=["DELETE"])
def delete_league(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM Leagues WHERE league_id = %s""", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "League deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@leagues_app.route("/leagues/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)
