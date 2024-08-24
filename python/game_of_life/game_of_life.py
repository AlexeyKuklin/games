#Game of Life
from random import binomialvariate
from os import system
from time import sleep

class CellType():
    DEAD = 0
    ALIVE = 1

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.init_cells() 

    def init_cells(self):
        return [CellType.DEAD for _ in range(self.width * self.height)]

    def get_cell(self, x, y):
        x = self.width + x if x < 0 else x
        x = x - self.width if x >= self.width else x 
        y = self.height + y if y < 0 else y
        y = y - self.height if y >= self.height else y
        return self.cells[y * self.width + x]

    def set_cell(self, cells, x, y, cell_type):
        cells[y * self.width + x] = cell_type

    def count_alive_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.get_cell(x + i, y + j) == CellType.ALIVE:
                    count += 1
        return count

    def set_random_board(self):
        for y in range(self.height):
            for x in range(self.width):
                self.set_cell(self.cells, x, y, CellType.ALIVE if binomialvariate(1, 0.2) == 1 else CellType.DEAD)


    def set_from_list(self, alive_list):
        for x, y in alive_list:
            self.set_cell(self.cells, x, y, CellType.ALIVE)

    def print_board(self):
        for y in range(self.height):
            s = []
            for x in range(self.width):
                s.append('O' if self.get_cell(x, y) == CellType.ALIVE else ' ')
            print(''.join(s))

    def one_step(self):
        system('clear')
        tmps = self.init_cells()
        for y in range(self.height):
            for x in range(self.width):
                count = self.count_alive_neighbors(x, y)
                if self.get_cell(x, y) == CellType.ALIVE:
                    if 2 <= count <= 3:
                        self.set_cell(tmps, x, y, CellType.ALIVE)
                else:
                    if count == 3:
                        self.set_cell(tmps, x, y, CellType.ALIVE)

        self.cells = tmps
        self.print_board()

    def play(self):
        while True:
            self.one_step()
            #input("Press enter to continue...")
            sleep(0.3)

board = Board(150, 40)
board.set_random_board()
#board.set_from_list([(10, 10), (10, 11), (10, 12)])
#board.set_from_list([(20, 10), (20, 11), (21, 10), (21, 11)])
board.play()
