from flask import Flask, request, render_template
from sitelogic.security.validateSignature import is_valid_signature
from sitelogic.chess.game import Game
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv
import git

app = Flask(__name__, static_url_path="/static/")

load_dotenv(".env")

user = "LordLlamaIII"
sqlpass = getenv("SQL_PASS")
host = "LordLlamaIII.mysql.pythonanywhere-services.com"
dbname = "LordLlamaIII$cfoster"
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{user}:{sqlpass}@{host}/{dbname}"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class ChessDB(db.Model):
    __tablename__ = "chess"
    id = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.String(8))
    content = db.Column(db.String(4096))

@app.route("/")
def renderSlash():
    out = render_template("home.html")
    return out

@app.route("/chess", methods=["GET", "POST"])
def renderChess():
    if request.form.get("tryMove"):
        fen = request.form.get("fen")
        turn = request.form.get("turn")
        start = request.form.get("start")
        end = request.form.get("end")
        enpassant = request.form.get("enpassant")

        game = Game(fen, turn, start, end, enpassant)
        valid = game.tryMove()
        promotion = game.getPromotion()
        fen = game.encodeFEN() if valid else fen
        enpassant = game.encodeEnpassant()
        checkmate = game.checkmate

        out = f"{fen}\n{enpassant}\n{promotion}\n{checkmate}"

    elif request.args.get("c"):
        gameid = request.args.get("c")
        game = ChessDB(content=gameid)
        db.session.add(game)
        db.session.commit()

        out = render_template("chess.html", data=ChessDB.query.all())

    else:
        out = render_template("chess.html", data="\"\"")

    return out

@app.route("/update_server", methods=["POST"])
def webhook():
    out = ("Update Failed", 400)

    if request.method == "POST":
        x_hub_signature = request.headers.get("X-Hub-Signature")
        w_secret = getenv("SECRET_TOKEN")

        if is_valid_signature(x_hub_signature, request.data, w_secret):
            repo = git.Repo("mysite")
            origin = repo.remotes.origin
            git_ssh_identity_file = "../.ssh/id_rsa"
            git_ssh_cmd = f"ssh -i {git_ssh_identity_file}"

            with git.Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
                origin.pull()

            out = ("Updated Successfully", 200)

    return out
