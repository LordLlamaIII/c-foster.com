from sitelogic.chess import piece as piecelib
from math import dist
from itertools import zip_longest as zipLong

class Board:

    def __init__(self, fen, enpassant):
        self.board = self.buildBoard(fen)
        self.enpassant = enpassant if enpassant else []

    def buildBoard(self, fen):
        numToSpaceArgs = [(str(n), " " * n) for n in range(1, 9)]

        for args in numToSpaceArgs:
            fen = fen.replace(*args)

        board = [list(row) for row in fen.split("/")]

        for row in range(8):
            for col in range(8):
                piece = board[row][col]

                if piece != " ":
                    board[row][col] = piecelib.Piece(piece, row, col)

        return board

    def getPiece(self, row, col):
        piece = self.board[row][col]

        return piece

    def findKings(self):
        flatString = str(self).replace("\n", "")
        rowK = flatString.find("K") // 8
        colK = flatString.find("K") % 8
        rowk = flatString.find("k") // 8
        colk = flatString.find("k") % 8

        kings = [(rowK, colK), (rowk, colk)]

        return kings

    def getPieceInfo(self, row, col):
        piece = self.board[row][col]
        pieceInfo = piece.getInfo() if piece != " " else "empty"

        return pieceInfo

    def setPiece(self, row, col, symbol):
        piece = piecelib.Piece(symbol, row, col)
        self.board[row][col] = piece

        return piece

    def movePiece(self, rowI, colI, rowF, colF, player):
        piece = self.board[rowI][colI]
        target = self.board[rowF][colF]

        valid = piece.move(rowF, colF, target, player=player)

        if piece.getKind() not in ["pawn", "knight"]:
            closest = self.projectFromPiece(rowI, colI, rowF, colF)
            valid = False if closest != [rowF, colF] else valid

        if valid and valid not in ["castle", "move2"]:
            self.board[rowF][colF] = piece
            self.board[rowI][colI] = " "

        elif valid == "castle":
            direction = 1 if colF == 7 else -1
            self.board[rowI][colI] = " "
            self.board[rowF][colF] = " "
            self.board[rowI][colI + direction * 2] = piece
            self.board[rowI][colI + direction] = target
            valid = bool(valid)

        elif valid == "move2":
            direction = 1 if rowI == 1 else -1
            self.board[rowF][colF] = piece
            self.board[rowI][colI] = " "
            self.enpassant.append([rowF, colF, rowI + direction, colI])

        if len(self.enpassant) >= 1 and (valid or piece.getKind() == "pawn"):
            for i in range(len(self.enpassant) - 1, -1, -1):
                if rowI == self.enpassant[i][0] and colI == self.enpassant[i][1]:
                    self.enpassant.pop(i)

                elif rowF == self.enpassant[i][2] and colF == self.enpassant[i][3]:
                    if piece.getKind() == "pawn":
                        target = self.board[self.enpassant[i][0]][self.enpassant[i][1]]
                        valid = piece.move(rowF, colF, target, player=player)

                        if valid:
                            self.board[rowF][colF] = piece
                            self.board[rowI][colI] = " "

                        else:
                            return valid

                    self.board[self.enpassant[i][0]][self.enpassant[i][1]] = " "
                    self.enpassant.pop(i)

        return valid

    def testMove(self, rowI, colI, rowF, colF):
        piece = self.board[rowI][colI]
        target = self.board[rowF][colF]

        valid = piece.move(rowF, colF, target)

        if piece.getKind() not in ["pawn", "knight"]:
            closest = self.projectFromPiece(rowI, colI, rowF, colF)
            valid = False if closest != [rowF, colF] else valid

        return valid

    def projectFromPiece(self, rowI, colI, rowF, colF):
        piecesInPath = []
        dR = 1 if rowF - rowI < 0 else -1
        dC = 1 if colF - colI < 0 else -1
        fill = 0

        if rowI == rowF:
            fill = rowI

        elif colI == colF:
            fill = colI

        coords = zipLong(range(rowF, rowI, dR), range(colF, colI, dC), fillvalue=fill)

        for (r, c) in coords:
            piece = self.board[r][c]

            if piece != " ":
                piecesInPath.append([r, c])

        if not piecesInPath:
            return [rowF, colF]

        distanceList = [dist([rowI, colI], coord) for coord in piecesInPath]
        closest = piecesInPath[distanceList.index(min(distanceList))]

        return closest

    def __str__(self):
        stringBoard = [[str(piece) for piece in row] for row in self.board]
        stringOut = "\n".join(["".join(row) for row in stringBoard])

        return str(stringOut)
