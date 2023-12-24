from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

games_app = Blueprint('games', __name__)

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

@games_app.route("/games", methods=["GET"])
def get_games():
    data = data_fetch("""SELECT * FROM games""")
    return make_response(jsonify(data), 200)

@games_app.route("/games/<int:game_code>", methods=["GET"])
def get_games_by_id(game_code):
    data = data_fetch("""SELECT * FROM games WHERE game_code = {}""".format(game_code))
    return make_response(jsonify(data), 200)

@games_app.route("/games/<int:game_code>/games", methods=["GET"])
def get_game_by_player(game_code):
    data = data_fetch(
        """
        SELECT
            PG.player_id,
            P.first_name,
            P.last_name,
            PG.game_code,
            G.game_name,
            PG.ranking
        FROM
            Players_Game_Ranking PG
        JOIN
            Players P ON PG.player_id = P.player_id
        JOIN
            Games G ON PG.game_code = G.game_code
        WHERE
            PG.game_code = {}
        """.format(game_code)
    )
    return make_response(
        jsonify({"game_code": game_code, "count": len(data), "games": data}), 200
    )


@games_app.route("/games", methods=["POST"])
def add_games():
    cur = mysql.connection.cursor()
    info = request.get_json()
    game_code = info["game_code"]
    game_name = info["game_name"]
    game_description = info["game_description"]
    cur.execute(
        """INSERT INTO games (game_code, game_name, game_description) VALUES (%s, %s, %s)""",
        (game_code, game_name, game_description),
    )
    mysql.connection.commit()
    print("row(s) affected: {}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "player added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@games_app.route("/games/<int:game_code>", methods=["PUT"])
def update_games(game_code):
    cur = mysql.connection.cursor()
    info = request.get_json()
    game_name = info["game_name"]
    game_description = info["game_description"]
    cur.execute(
        """UPDATE games SET game_name = %s, game_description = %s WHERE game_code = %s""",
        (game_name, game_description, game_code),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Game updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@games_app.route("/games/<int:game_code>", methods=["DELETE"])
def delete_games(game_code):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM games WHERE game_code = %s""", (game_code,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "game deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@games_app.route("/games/format", methods=["GET"])
def get_params():
    fmt = request.args.get('game_code')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)
