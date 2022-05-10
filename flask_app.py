from flask import Flask, request, render_template
from sitelogic.chess.game import Game

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
