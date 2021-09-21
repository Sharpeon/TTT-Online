import random

class Game:
    def __init__(self, id) -> None:
        self.id = id
        self.turnP1 = random.choice([True, False])
        self.rows = 3
        self.cols = 3
        self.grid = [[-1 for i in range(self.cols)] for j in range(self.rows)]  # 2d arrays are weird in python...
        self.last_winner = None

    def resetGame(self):
        self.turnP1 = random.choice([True, False])
        self.grid = [[-1 for i in range(self.cols)] for j in range(self.rows)]

    def placeSymbol(self, pos:int, symbol:str):
        finalPos = 0

        for x in range(self.rows):
            for y in range(self.cols):
                if finalPos == pos:
                    self.grid[x][y] = symbol
                    return
                else:
                    finalPos += 1

        self.switchTurn()

    def switchTurn(self):
        self.turn1 = not self.turnP1

    def checkWin(self, symbol:str) -> bool:
        count = 0

        # Check Horizontal wins
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[y][x] == symbol:
                    count += 1
            if count == self.cols:
                count = 0
                return True
            else:
                count = 0

        # Check Vertical wins
        for x in range(self.cols):
            for y in range(self.rows):
                if self.grid[x][y] == symbol:
                    count += 1
            if count == self.rows:
                count = 0
                return True
            else:
                count = 0

        # Check win diagonal like \
        for i in range(self.cols):
            if self.grid[i][i] == symbol:
                count += 1
        if count == self.cols:
            return True
        else:
            count = 0

        # Check win diagonal like /
        row = 0
        for i in reversed(range(self.cols)):
            if self.grid[i][row] == symbol:
                count += 1
            row += 1
        if count == self.cols:
            return True

        return False

game = Game(1)
