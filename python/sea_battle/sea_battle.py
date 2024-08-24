#Sea Battle game
import os
import random

class CellType:
    EMPTY = 0
    SHIP = 1
    MISS = 2
    HIT = 3
    DEAD = 4

class ShipOrientation:
    HORIZONTAL = 0
    VERTICAL = 1

class Cell:
    def __init__(self, x, y, cell_type):
        self.x = x
        self.y = y
        self.cell_type = cell_type

class Ship:
    def __init__(self, x, y, length, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.cells = []
        for i in range(length):
            if orientation == ShipOrientation.HORIZONTAL:
                self.cells.append(Cell(x + i, y, CellType.SHIP))
            else:
                self.cells.append(Cell(x, y + i, CellType.SHIP))

    @property
    def is_alive(self):
        for cell in self.cells:
            if cell.cell_type == CellType.SHIP:
                return True
        return False
    
    @property
    def length(self):
        return len(self.cells)


class Board:
    ship_lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]   
    cell_mapping = {
        CellType.EMPTY: ' ',
        CellType.SHIP:  'O',
        CellType.HIT:   'X',
        CellType.MISS:  '*'
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [
            Cell(x, y, CellType.EMPTY) 
            for x in range(self.width) 
            for y in range(self.height)
        ]

    def clear(self):
        for cell in self.cells:
            cell.cell_type = CellType.EMPTY

    @property
    def is_alive(self):
        for cell in self.cells:
            if cell.cell_type == CellType.SHIP:
                return True
        return False

    def is_cell_in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_cell_empty(self, x, y):
        cell = self.get_cell(x, y)
        if cell is None or cell.cell_type == CellType.EMPTY:
            return True
        return False

    def is_cell_valid(self, x, y):
        return self.is_cell_in_bounds(x, y) and self.get_cell(x, y).cell_type == CellType.EMPTY
    
    def is_surrounded(self, x, y):
        if not self.is_cell_valid(x, y):
            return False

        for i in range(-1, 2):
            for j in range(-1, 2):
                if not self.is_cell_empty(x + i, y + j):
                    return False
        return True
    
    def get_cell(self, x, y):
        return self.cells[y * self.width + x] if self.is_cell_in_bounds(x, y) else None

    def set_cell(self, x, y, cell_type):
        self.cells[y * self.width + x].cell_type = cell_type

    def place_ship(self, ship: Ship) -> bool:
        for cell in ship.cells:
            if not self.is_surrounded(cell.x, cell.y):
                return False
        
        for cell in ship.cells:
            self.set_cell(cell.x, cell.y, cell.cell_type)
        return True

    def get_random_ship(self, ship_length):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        orientation = random.choice([ShipOrientation.HORIZONTAL, ShipOrientation.VERTICAL])
        return Ship(x, y, ship_length, orientation)      
    
    def try_place_ship(self, ship_length, try_count=10):
        for _ in range(try_count):
            ship = self.get_random_ship(ship_length)
            if self.place_ship(ship):
                return ship
        return None

    def place_random_ships(self):
        ships = []
        while len(ships) != len(Board.ship_lengths):
            self.clear()
            for ship_length in Board.ship_lengths:
                if ship := self.try_place_ship(ship_length):
                    ships.append(ship)
                else:
                    ships = []
                    break
        return ships                
    
    @staticmethod
    def board_to_2d_representation(board: "Board") -> list[list[str]]:
        out = []
        for y in range(board.height):
            row = []
            for x in range(board.width):
                cell_type = board.get_cell(x, y).cell_type
                row.append(Board.cell_mapping[cell_type])
            out.append(row)
        return out

    @staticmethod
    def row_to_str(i, row):
        return f"{i+1:>2}\033[4;36;44m|{"|".join(row)}|\033[0m"   

    @staticmethod
    def print_boards(board_player, board_enemy):
        board_left = Board.board_to_2d_representation(board_player)
        board_right = Board.board_to_2d_representation(board_enemy)
        s = []
        for i, row in enumerate(range(board_player.height)):
            s.append(Board.row_to_str(i, board_left[row]))
            s.append("   ")
            s.append(Board.row_to_str(i, board_right[row]))
            print("".join(s))
            s = []
        print("   a b c d e f g h i j       a b c d e f g h i j")

    def get_secret_board(self):
        board = Board(self.width, self.height)
        for cell in self.cells:
            board.set_cell(cell.x, cell.y, cell_type = CellType.EMPTY if cell.cell_type == CellType.SHIP else cell.cell_type)
        return board


class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board(10, 10)
        self.enemy_board = Board(10, 10)
        self.ships = self.board.place_random_ships()


    @staticmethod
    def process_input(s):
        x = s[0].lower() 
        y = s[1:]
        return int(y) - 1, ord(x) - ord("a")
    
    @staticmethod
    def decode_output(x, y):
        return chr(y + ord("a")) + str(x + 1)
    

    def hit(self, x, y):
        if self.board.get_cell(x, y).cell_type == CellType.SHIP:
            self.board.set_cell(x, y, CellType.HIT)
            return True
        else:
            self.board.set_cell(x, y, CellType.MISS)
            return False

    def random_shot(self):
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        for _ in range(100):
            if self.enemy_board.get_cell(x, y).cell_type == CellType.EMPTY:
                return x, y
        
        for x in range(10):
            for y in range(10):
                if self.enemy_board.get_cell(x, y).cell_type == CellType.EMPTY:
                    return x, y        



class Game:
    def __init__(self, player1_name="Player1", player2_name="Player2"):
        self.players = [Player(player1_name), Player(player2_name)]
        player_index = 0 #random.randint(0, 1)
        self.player = self.players[player_index]
        self.other_player = self.players[1 - player_index]       

    def change_player(self):
        self.player, self.other_player = self.other_player, self.player

    def clear_screen(self):
        os.system('clear')
        print("Sea Battle")
        print(f"{self.player.name}'s turn")

    def process_input(self):
        if self.player.name == "PlayerAI":
            x, y = self.player.random_shot()
        else:
            s = input("Your shot: ")
            x, y = Player.process_input(s)
        
        return x, y


    def is_game_running(self):
        return self.player.board.is_alive and self.other_player.board.is_alive


    def play_with_AI(self):
        while self.is_game_running():
            self.clear_screen()
            Board.print_boards(self.player.board, self.other_player.board.get_secret_board())
            x, y = self.process_input()
            hit_result = self.other_player.hit(x, y)
            
            self.clear_screen()
            Board.print_boards(self.player.board, self.other_player.board.get_secret_board())
            if hit_result:
                print(f"{self.player.name} hit {x}, {y} and {Player.decode_output(x, y)}")
            else:
                print(f"{self.player.name} missed {x}, {y} and {Player.decode_output(x, y)}")

            if self.player.name != "PlayerAI":
                input("Press enter to continue...")

            self.clear_screen()
            self.change_player()


if __name__ == "__main__":
    Game("alex", "PlayerAI").play_with_AI()
