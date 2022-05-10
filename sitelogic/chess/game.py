from sitelogic.chess import board
from itertools import product
from json import dumps, loads

class Game:

    def __init__(self, fen, turn, start, end, enpassant, fake=False):
        self.fake = fake
        self.board = board.Board(fen, loads(enpassant))
        self.turn = turn
        self.move = self.formatMove(start, end)
        self.danger = []
        self.check = ""
        self.checkmate = ""
        self.valid = False

    def tryMove(self):
        self.valid = self.board.movePiece(*self.move)
        self.evaluateCheck()
        self.evaluateCheckmate()

        self.valid = self.valid if self.check != self.turn else False

        return self.valid

    def encodeFEN(self):
        fen = str(self.board)
        fen = fen.replace("\n", "/")

        spaceToNumArgs = [(" " * n, str(n)) for n in range(8, 0, -1)]

        for args in spaceToNumArgs:
            fen = fen.replace(*args)

        return fen

    def encodeEnpassant(self):
        jsonpassant = dumps(self.board.enpassant)

        return jsonpassant

    def formatMove(self, start, end):
        if not self.fake:
            start = [8 - int(start[1]), ord(start[0]) - 97]
            end = [8 - int(end[1]), ord(end[0]) - 97]

        move = start + end + [self.turn]

        return move

    def getPromotion(self):
        row = self.move[2]
        col = self.move[3]
        piece = self.board.getPiece(row, col)

        if not self.valid or piece.getKind() != "pawn" or row not in [0, 7]:
            return "false"

        self.board.setPiece(row, col, "x")

        return "true"

    def evaluateDanger(self):
        for rowI, colI, rowF, colF in product(range(8), repeat=4):
            if self.board.getPiece(rowI, colI) != " ":
                target = self.board.getPiece(rowF, colF)
                canMove = self.board.testMove(rowI, colI, rowF, colF)

                if target != " " and canMove:
                    self.danger.append(target)

    def evaluateCheck(self):
        kings = self.board.findKings()

        if self.fake:
            color = 0 if self.turn == "black" else 1
            kings = kings[color:color + 1]

        for king in self.board.findKings():
            target = self.board.getPiece(*king)

            for rowI, colI in product(range(8), repeat=2):
                piece = self.board.getPiece(rowI, colI)

                if piece != " " and piece.getColor() != target.getColor():
                    canMove = self.board.testMove(rowI, colI, *king)

                    if canMove:
                        self.check = target.getColor()

        return self.check

    def evaluateCheckmate(self):
        if self.check and not self.fake:
            fen = self.encodeFEN()
            turn = "white" if self.turn == "black" else "black"
            canEscape = False

            for rowI, colI, rowF, colF in product(range(8), repeat=4):
                start = [rowI, colI]
                end = [rowF, colF]
                piece = self.board.getPiece(rowI, colI)

                if piece != " " and piece.getColor() == turn:
                    game = Game(fen, turn, start, end, self.encodeEnpassant(), fake=True)
                    game.tryMove()
                    canEscape = canEscape if game.check == turn else True

                    if canEscape:
                        break

            if not canEscape:
                self.checkmate = turn

        return self.checkmate
