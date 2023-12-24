#teams
from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

teams_app = Blueprint('teams', __name__)

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

@teams_app.route("/teams", methods=["GET"])
def get_teams():
    data = data_fetch("""SELECT * FROM Teams""")
    return make_response(jsonify(data), 200)

@teams_app.route("/teams/<int:id>", methods=["GET"])
def get_team_by_id(id):
    data = data_fetch("""SELECT * FROM Teams WHERE team_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@teams_app.route("/teams", methods=["POST"])
def add_team():
    cur = mysql.connection.cursor()
    info = request.get_json()
    team_id = info["team_id"]
    created_by_player_id = info["created_by_player_id"]
    team_name = info["team_name"]
    date_created = info["date_created"]
    date_disbanded = info["date_disbanded"]
    cur.execute(
        """INSERT INTO Teams (team_id, created_by_player_id, team_name, date_created, date_disbanded)
           VALUES (%s, %s, %s, %s, %s)""",
        (team_id, created_by_player_id, team_name, date_created, date_disbanded),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "team added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@teams_app.route("/teams/<int:id>", methods=["PUT"])
def update_team(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    created_by_player_id = info["created_by_player_id"]
    team_name = info["team_name"]
    date_created = info["date_created"]
    date_disbanded = info["date_disbanded"]
    cur.execute(
        """UPDATE Teams SET created_by_player_id = %s, team_name = %s, date_created = %s,
           date_disbanded = %s WHERE team_id = %s""",
        (created_by_player_id, team_name, date_created, date_disbanded, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Team updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@teams_app.route("/teams/<int:id>", methods=["DELETE"])
def delete_team(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM Teams WHERE team_id = %s""", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Team deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@teams_app.route("/teams/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)
