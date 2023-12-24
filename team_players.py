# team_players

from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

team_players_app = Blueprint('team_players', __name__)

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

@team_players_app.route("/team_players", methods=["GET"])
def get_team_players():
    data = data_fetch("""SELECT * FROM Team_Players""")
    return make_response(jsonify(data), 200)

@team_players_app.route("/team_players/<int:team_id>/<int:player_id>", methods=["GET"])
def get_team_player(team_id, player_id):
    data = data_fetch(
        """SELECT * FROM Team_Players WHERE team_id = {} AND player_id = {}""".format(team_id, player_id)
    )
    return make_response(jsonify(data), 200)

@team_players_app.route("/team_players", methods=["POST"])
def add_team_player():
    cur = mysql.connection.cursor()
    info = request.get_json()
    team_id = info["team_id"]
    player_id = info["player_id"]
    date_from = info["date_from"]
    date_to = info["date_to"]
    cur.execute(
        """INSERT INTO Team_Players (team_id, player_id, date_from, date_to)
           VALUES (%s, %s, %s, %s)""",
        (team_id, player_id, date_from, date_to),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "team player added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@team_players_app.route("/team_players/<int:team_id>/<int:player_id>", methods=["PUT"])
def update_team_player(team_id, player_id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    date_from = info["date_from"]
    date_to = info["date_to"]
    cur.execute(
        """UPDATE Team_Players SET date_from = %s, date_to = %s
           WHERE team_id = %s AND player_id = %s""",
        (date_from, date_to, team_id, player_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Team player updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@team_players_app.route("/team_players/<int:team_id>/<int:player_id>", methods=["DELETE"])
def delete_team_player(team_id, player_id):
    cur = mysql.connection.cursor()
    cur.execute(
        """DELETE FROM Team_Players WHERE team_id = %s AND player_id = %s""",
        (team_id, player_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Team player deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@team_players_app.route("/team_players/format", methods=["GET"])
def get_params():
    fmt = request.args.get('team_id, player_id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)