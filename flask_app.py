from flask import Flask, request, render_template
from sitelogic.chess.game import Game
import git

app = Flask(__name__, static_url_path="/static/")

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
        out = render_template("chess.html")

    else:
        out = render_template("chess.html")

    return out

@app.route("/update_server", methods=["POST"])
def webhook():
    if request.method == "POST":
        repo = git.Repo("mysite")
        origin = repo.remotes.origin
        git_ssh_identity_file = "../.ssh/id_rsa"
        git_ssh_cmd = f"ssh -i {git_ssh_identity_file}"

        with git.Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
            origin.pull()

        out = ("Updated Successfully", 200)

    else:
        out = ("Update Failed", 400)

    return out
