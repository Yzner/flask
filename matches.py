from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

matches_app = Blueprint('matches', __name__)

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

@matches_app.route("/matches", methods=["GET"])
def get_matches():
    data = data_fetch("""SELECT * FROM Matches""")
    return make_response(jsonify(data), 200)

@matches_app.route("/matches/<int:match_id>", methods=["GET"])
def get_match_by_id(match_id):
    data = data_fetch("""SELECT * FROM Matches WHERE match_id = {}""".format(match_id))
    return make_response(jsonify(data), 200)

@matches_app.route("/matches", methods=["POST"])
def add_match():
    cur = mysql.connection.cursor()
    info = request.get_json()
    match_id = info["match_id"]
    game_code = info["game_code"]
    player_1_id = info["player_1_id"]
    player_2_id = info["player_2_id"]
    match_date = info["match_date"]
    result = info["result"]
    cur.execute(
        """INSERT INTO Matches (match_id, game_code, player_1_id, player_2_id, match_date, result)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (match_id, game_code, player_1_id, player_2_id, match_date, result),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "match added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@matches_app.route("/matches/<int:match_id>", methods=["PUT"])
def update_match(match_id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    game_code = info["game_code"]
    player_1_id = info["player_1_id"]
    player_2_id = info["player_2_id"]
    match_date = info["match_date"]
    result = info["result"]
    cur.execute(
        """UPDATE Matches SET game_code = %s, player_1_id = %s, player_2_id = %s,
           match_date = %s, result = %s WHERE match_id = %s""",
        (game_code, player_1_id, player_2_id, match_date, result, match_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Match updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@matches_app.route("/matches/<int:match_id>", methods=["DELETE"])
def delete_match(match_id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM Matches WHERE match_id = %s""", (match_id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Match deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@matches_app.route("/matches/format", methods=["GET"])
def get_params():
    fmt = request.args.get('match_id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)
