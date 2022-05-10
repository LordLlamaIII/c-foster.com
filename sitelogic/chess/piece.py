from math import dist, sqrt

class Piece:

    def __init__(self, symbol, row, col):
        self.kind, self.color = self.interpretSymbol(symbol)
        self.stringRepresentation = symbol
        self.row = row
        self.col = col

    def interpretSymbol(self, symbol):
        kind = ""
        lowSym = symbol.lower()

        if lowSym == "p":
            kind = "pawn"

        elif lowSym == "r":
            kind = "rook"

        elif lowSym == "n":
            kind = "knight"

        elif lowSym == "b":
            kind = "bishop"

        elif lowSym == "q":
            kind = "queen"

        elif lowSym == "k":
            kind = "king"

        color = "white" if symbol.isupper() else "black"

        return kind, color

    def getInfo(self):
        info = f"{self.color} {self.kind} {self.row}, {self.col}"

        return info

    def getKind(self):
        return self.kind

    def getColor(self):
        return self.color

    def move(self, row, col, target, player=None):
        valid = True
        distance = dist([self.row, self.col], [row, col])

        if player and player != self.getColor():
            return False

        elif row == self.row and col == self.col:
            return False

        elif row >= 8 or col >= 8:
            return False

        elif not (type(target) == type(self) or target == " "):
            return False

        elif target != " " and target.getColor() == self.color and self.kind != "king":
            return False

        if self.kind == "pawn":
            if self.color == "white" and self.row - row < 0:
                return False

            elif self.color == "black" and self.row - row > 0:
                return False

            elif target != " " and distance != sqrt(2):
                return False

            elif col != self.col and target == " ":
                return False

            elif self.color == "white" and distance >= 2 and self.row != 6:
                return False

            elif self.color == "black" and distance >= 2 and self.row != 1:
                return False

            elif distance > 2:
                return False

            if distance == 2:
                valid = "move2"

        elif self.kind == "rook":
            if row != self.row and col != self.col:
                return False

        elif self.kind == "knight":
            if distance != dist([0, 0], [1, 2]):
                return False

        elif self.kind == "bishop":
            if round(distance / sqrt(2), 5) != abs(self.row - row):
                return False

        elif self.kind == "queen":
            rookCondition = row != self.row and col != self.col
            bishopCondition = round(distance / sqrt(2), 5) != abs(self.row - row)

            if rookCondition and bishopCondition:
                return False

        elif self.kind == "king":
            castle = target != " "

            if castle:
                castle = self.kind == "king" and \
                         target.getKind() == "rook" and \
                         self.color == target.getColor()

            if distance >= 2 and not castle:
                return False

            elif str(target).isupper() == str(self).isupper() and not castle:
                return False

            if castle:
                valid = "castle"

        if player:
            self.row = row
            self.col = col

        return valid

    def __str__(self):
        return self.stringRepresentation
