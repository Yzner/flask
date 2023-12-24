#Players
from flask import Blueprint, make_response, jsonify, request
from flask_mysqldb import MySQL

players_app = Blueprint('players', __name__)

# Configure MySQL
mysql = MySQL()

@players_app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@players_app.route("/players", methods=["GET"])
def get_players():
    data = data_fetch("""SELECT * FROM players""")
    return make_response(jsonify(data), 200)

@players_app.route("/players/<int:id>", methods=["GET"])
def get_player_by_id(id):
    data = data_fetch("""SELECT * FROM players WHERE player_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@players_app.route("/players/<int:id>/matches", methods=["GET"])
def get_matches_by_player(id):
    data = data_fetch(
        """
        SELECT
            P.player_id,
            P.first_name,
            P.last_name,
            M.match_date,
            M.result
        FROM
            Players P
        JOIN
            Matches M ON P.player_id = M.player_1_id OR P.player_id = M.player_2_id
        WHERE
            (P.player_id, M.match_date) IN (
                SELECT
                    player_id,
                    MAX(match_date) AS max_date
                FROM
                    Players
                JOIN
                    Matches ON Players.player_id = Matches.player_1_id OR Players.player_id = Matches.player_2_id
                GROUP BY
                    player_id 
            );
        """.format(id)
    )
    return make_response(
        jsonify({"player_id": id, "count": len(data), "matches": data}), 200
    )


@players_app.route("/players/<int:id>/result", methods=["GET"])
def get_results_by_player(id):
    query = """
        SELECT 
            Players.player_id,
            Players.first_name,
            Players.last_name,
            Players.gender,
            Players.address,
            Matches.match_id,
            Matches.game_code,
            Games.game_name,
            Matches.player_1_id,
            Matches.player_2_id,
            Matches.match_date,
            Matches.result
        FROM Players
        LEFT JOIN Matches ON Players.player_id = Matches.player_1_id OR Players.player_id = Matches.player_2_id
        LEFT JOIN Games ON Matches.game_code = Games.game_code
        WHERE Players.player_id = {};
    """.format(id)

    data = data_fetch(query)
    return make_response(
        jsonify({"player_id": id, "count": len(data), "results": data}), 200
    )


@players_app.route("/players", methods=["POST"])
def add_players():
    cur = mysql.connection.cursor()
    info = request.get_json()
    player_id = info["player_id"]
    first_name = info["first_name"]
    last_name = info["last_name"]
    gender = info["gender"]
    address = info["address"]
    cur.execute(
        """INSERT INTO players (player_id, first_name, last_name, gender, address) VALUES (%s, %s, %s, %s, %s)""",
        (player_id, first_name, last_name, gender, address),
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

@players_app.route("/players/<int:id>", methods=["PUT"])
def update_players(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    gender = info["gender"]
    address = info["address"]
    cur.execute(
        """UPDATE players SET first_name = %s, last_name = %s, gender = %s, address = %s WHERE player_id = %s""",
        (first_name, last_name, gender, address, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Player updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@players_app.route("/players/<int:id>", methods=["DELETE"])
def delete_players(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM players WHERE player_id = %s""", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "player deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@players_app.route("/players/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)
