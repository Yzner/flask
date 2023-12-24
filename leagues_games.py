from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

leagues_games_app = Blueprint('leagues_games', __name__)

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

@leagues_games_app.route("/leagues_games", methods=["GET"])
def get_leagues_games():
    data = data_fetch("""SELECT * FROM Leagues_Games""")
    return make_response(jsonify(data), 200)

@leagues_games_app.route("/leagues_games/<int:league_id>/<int:game_code>", methods=["GET"])
def get_league_game(league_id, game_code):
    data = data_fetch(
        """SELECT * FROM Leagues_Games WHERE league_id = {} AND game_code = {}""".format(league_id, game_code)
    )
    return make_response(jsonify(data), 200)

@leagues_games_app.route("/leagues_games", methods=["POST"])
def add_league_game():
    cur = mysql.connection.cursor()
    info = request.get_json()
    league_id = info["league_id"]
    game_code = info["game_code"]
    cur.execute(
        """INSERT INTO Leagues_Games (league_id, game_code) VALUES (%s, %s)""",
        (league_id, game_code),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "league game added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@leagues_games_app.route("/leagues_games/<int:league_id>/<int:game_code>", methods=["DELETE"])
def delete_league_game(league_id, game_code):
    cur = mysql.connection.cursor()
    cur.execute(
        """DELETE FROM Leagues_Games WHERE league_id = %s AND game_code = %s""",
        (league_id, game_code),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "League game deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@leagues_games_app.route("/leagues_games/format", methods=["GET"])
def get_params():
    fmt = request.args.get('league_id, game_code')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)
