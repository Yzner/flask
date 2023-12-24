from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

players_game_ranking_app = Blueprint('players_game_ranking', __name__)

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

@players_game_ranking_app.route("/players_game_ranking", methods=["GET"])
def get_players_game_ranking():
    data = data_fetch("""SELECT * FROM Players_Game_Ranking""")
    return make_response(jsonify(data), 200)

@players_game_ranking_app.route("/players_game_ranking/<int:player_id>/<int:game_code>", methods=["GET"])
def get_player_game_ranking(player_id, game_code):
    data = data_fetch(
        """SELECT * FROM Players_Game_Ranking WHERE player_id = {} AND game_code = {}""".format(player_id, game_code)
    )
    return make_response(jsonify(data), 200)

@players_game_ranking_app.route("/players_game_ranking", methods=["POST"])
def add_player_game_ranking():
    cur = mysql.connection.cursor()
    info = request.get_json()
    player_id = info["player_id"]
    game_code = info["game_code"]
    ranking = info["ranking"]
    cur.execute(
        """INSERT INTO Players_Game_Ranking (player_id, game_code, ranking) VALUES (%s, %s, %s)""",
        (player_id, game_code, ranking),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "player game ranking added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@players_game_ranking_app.route("/players_game_ranking/<int:player_id>/<int:game_code>", methods=["PUT"])
def update_player_game_ranking(player_id, game_code):
    cur = mysql.connection.cursor()
    info = request.get_json()
    ranking = info["ranking"]
    cur.execute(
        """UPDATE Players_Game_Ranking SET ranking = %s WHERE player_id = %s AND game_code = %s""",
        (ranking, player_id, game_code),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Player game ranking updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@players_game_ranking_app.route("/players_game_ranking/<int:player_id>/<int:game_code>", methods=["DELETE"])
def delete_player_game_ranking(player_id, game_code):
    cur = mysql.connection.cursor()
    cur.execute(
        """DELETE FROM Players_Game_Ranking WHERE player_id = %s AND game_code = %s""",
        (player_id, game_code),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Player game ranking deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@players_game_ranking_app.route("/players_game_ranking/format", methods=["GET"])
def get_params():
    fmt = request.args.get('player_id, game_code')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)
