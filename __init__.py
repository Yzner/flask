from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "renz"
app.config["MYSQL_DB"] = "league"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Import the players blueprint
from .players import players_app
from .games import games_app
from .leagues import leagues_app
from .teams import teams_app
from .players_game_ranking import players_game_ranking_app
from .leagues_games import leagues_games_app
from .matches import matches_app
from .team_players import team_players_app

# Register the players blueprint
app.register_blueprint(players_app, url_prefix='/players')
app.register_blueprint(games_app, url_prefix='/games')
app.register_blueprint(leagues_app, url_prefix='/leagues')
app.register_blueprint(teams_app, url_prefix='/teams')
app.register_blueprint(players_game_ranking_app, url_prefix='/players_game_ranking')
app.register_blueprint(leagues_games_app, url_prefix='/leagues_games')
app.register_blueprint(matches_app, url_prefix='/matches')
app.register_blueprint(team_players_app, url_prefix='/team_players')
# Import the main module (main.py)
from . import main
