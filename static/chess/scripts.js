function pieceTheme(piece) {
    var img = "/static/chess/pieces/" + piece + ".png";
    return img;
}

function onDrop(source, target, piece, newPos, oldPos, orientation) {
    var fen = Chessboard.objToFen(oldPos);
    var url = "https://www.c-foster.com/chess";
    var data = {
        "tryMove": "true",
        "fen": fen,
        "turn": turn,
        "start": source,
        "end": target,
        "enpassant": enpassant
    };

    var result = $.post(url, data, function(result) {
        var resultFen = result.split("\n")[0];
        enpassant = result.split("\n")[1];
        promotion(resultFen, result.split("\n")[2]);
        var checkmate = result.split("\n")[3]

        board.position(resultFen);

        if (source !== target && resultFen !== fen) {
            turn = (turn !== "white") ? "white" : "black";
        }

        if (checkmate) {
            runCheckmate(checkmate);
        }
    });
}

function promotion(fen, promote) {
    if (promote == "false") { return; }

    promotionFen = fen;
    $("#option")[0].value = "";
    $(".pk-form").click();
    checkPromotionChange();
}

function checkPromotionChange() {
    var piece = $("#option")[0].value;

    if (piece !== "") {
        piece = (turn == "black") ? piece : piece.toLowerCase();

        var fen = promotionFen.replace("x", piece);
        return board.position(fen);
    }

    else {
        return setTimeout(checkPromotionChange, 50);
    }
}

function runCheckmate(side) {
    var winner = (side == "black") ? "White" : "Black";
    $("#overlay").css("visibility", "visible");
    $("#winner").text(winner + " wins.");
    $("#wintext").css("visibility", "visible");
}

function newGame() {
    $("#wintext").css("visibility", "hidden");
    $("#winner").text("");
    $("#overlay").css("visibility", "hidden");

    board.position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR");
    turn = "white";
    enpassant = "[]";
    promotionFen = "";
}

function invite() {
    console.log("This is not implemented yet. :(");
    var code = Math.random().toString(36).slice(2, 10);
    var url = "https://www.c-foster.com/chess?c=" + code;
    navigator.clipboard.writeText(url);
}

function createBoard() {
    var config = {
        pieceTheme: pieceTheme,
        position: "start",
        draggable: true,
        onDrop: onDrop
    };

    board = new Chessboard("board", config);
}

function startPickout() {
    pickout.to({
        el: ".option",
        theme: "dark"
    });
}

function setButtons() {
    $("#invite").click(invite);
    $("#playagain").click(newGame);
    console.log("test2!");
}

var board;
var turn = "white";
var enpassant = "[]";
var promotionFen = "";
$(document).ready(createBoard);
$(document).ready(startPickout);
$(document).ready(setButtons);
