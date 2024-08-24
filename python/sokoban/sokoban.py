#Sokoban

import pygame

class Cell:
    EMPTY = 0
    WALL = 1
    BOX = 2
    PLAYER = 3
    TARGET = 4
    BOX_TARGET = 5
    PLAYER_TARGET = 6
    NONE = 7

class Board:
    movs = {
        (Cell.PLAYER, Cell.EMPTY): (Cell.EMPTY, Cell.PLAYER),
        (Cell.PLAYER, Cell.TARGET): (Cell.EMPTY, Cell.PLAYER_TARGET),
        (Cell.PLAYER_TARGET, Cell.EMPTY): (Cell.TARGET, Cell.PLAYER),
        (Cell.PLAYER_TARGET, Cell.TARGET): (Cell.TARGET, Cell.PLAYER_TARGET),
        (Cell.BOX, Cell.EMPTY): (Cell.EMPTY, Cell.BOX),
        (Cell.BOX, Cell.TARGET): (Cell.EMPTY, Cell.BOX_TARGET),
        (Cell.BOX_TARGET, Cell.EMPTY): (Cell.TARGET, Cell.BOX),
        (Cell.BOX_TARGET, Cell.TARGET): (Cell.TARGET, Cell.BOX_TARGET),
    }    

    def __init__(self, level):
        self.load_from_array(level)

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y*self.width + x]
        return None

    def set_cell(self, x, y, cell_type):
        self.map[y*self.width + x] = cell_type    

    def load_from_array(self, array):
        self.width = len(array[0])
        self.height = len(array)
        self.map = [Cell.EMPTY]*(self.width*self.height)
        for y in range(self.height):
            for x in range(self.width):
                if array[y][x] == Cell.PLAYER:
                    self.player_xy = (x, y)
                self.map[y*self.width + x] = array[y][x]

    def move(self, dx, dy):
        x, y = self.player_xy
        cell_cur = self.get_cell(x, y)
        cell_nxt = self.get_cell(x + dx, y + dy)
        mov = self.movs.get((cell_cur, cell_nxt))
        if mov:
            cell_cur, cell_nxt = mov
            self.set_cell(x, y, cell_cur)
            self.set_cell(x + dx, y + dy, cell_nxt)
            self.player_xy = (x + dx, y + dy)
            return True
        
        cell_nxt_nxt = self.get_cell(x + 2*dx, y + 2*dy)
        mov = self.movs.get((cell_nxt, cell_nxt_nxt))
        if mov:
            cell_nxt, cell_nxt_nxt = mov
            mov = self.movs.get((cell_cur, cell_nxt))
            if mov:
                cell_cur, cell_nxt = mov
                self.set_cell(x, y, cell_cur)
                self.set_cell(x + dx, y + dy, cell_nxt)
                self.set_cell(x + 2*dx, y + 2*dy, cell_nxt_nxt)
                self.player_xy = (x + dx, y + dy)
                return True

        return False

    def is_level_finished(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y) in [Cell.TARGET, Cell.PLAYER_TARGET]:
                    return False
        return True


class Game:
    tiles = {
        Cell.WALL: pygame.image.load('sokoban/resources/wall.png'),
        Cell.TARGET: pygame.image.load('sokoban/resources/target.png'),
        Cell.BOX: pygame.image.load('sokoban/resources/box.png'),
        Cell.PLAYER: pygame.image.load('sokoban/resources/player.png'),
        Cell.EMPTY: pygame.image.load('sokoban/resources/empty.png'),
        Cell.BOX_TARGET: pygame.image.load('sokoban/resources/box_target.png'),
        Cell.PLAYER_TARGET: pygame.image.load('sokoban/resources/player_target.png')
    }

    level1 = [
        [Cell.NONE, Cell.NONE,   Cell.WALL,   Cell.WALL,       Cell.WALL,   Cell.WALL,   Cell.WALL,   Cell.NONE],
        [Cell.WALL, Cell.WALL,   Cell.WALL,   Cell.EMPTY,      Cell.EMPTY,  Cell.EMPTY,  Cell.WALL,   Cell.NONE],
        [Cell.WALL, Cell.TARGET, Cell.PLAYER, Cell.BOX,        Cell.EMPTY,  Cell.EMPTY,  Cell.WALL,   Cell.NONE],
        [Cell.WALL, Cell.WALL,   Cell.WALL,   Cell.EMPTY,      Cell.BOX,    Cell.TARGET, Cell.WALL,   Cell.NONE],
        [Cell.WALL, Cell.TARGET, Cell.WALL,   Cell.WALL,       Cell.BOX  ,  Cell.EMPTY,  Cell.WALL,   Cell.NONE],
        [Cell.WALL, Cell.EMPTY,  Cell.WALL,   Cell.EMPTY,      Cell.TARGET, Cell.EMPTY,  Cell.WALL,   Cell.WALL],
        [Cell.WALL, Cell.BOX,    Cell.EMPTY,  Cell.BOX_TARGET, Cell.BOX,    Cell.BOX,    Cell.TARGET, Cell.WALL],
        [Cell.WALL, Cell.EMPTY,  Cell.EMPTY,  Cell.EMPTY,      Cell.TARGET, Cell.EMPTY,  Cell.EMPTY,  Cell.WALL],
        [Cell.WALL, Cell.WALL,   Cell.WALL,   Cell.WALL,       Cell.WALL,   Cell.WALL,   Cell.WALL,   Cell.WALL]
    ]

    def __init__(self, level=None):
        pygame.init()
        pygame.display.set_caption("Sokoban")
        self.init(Game.level1)

    def init(self, level):
        self.is_game_running = True
        self.is_level_complete = False
        self.board = Board(level)
        
    def handle_events(self, board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    board.move(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    board.move(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    board.move(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    board.move(1, 0)
                elif event.key == pygame.K_ESCAPE:
                    self.init(Game.level1)

    def update(self, board):
        self.is_level_complete = board.is_level_finished()

    def draw(self, screen, board):
        screen.fill((0, 0, 0))
        x0 = (screen.get_width() - board.width * 32) // 2
        y0 = (screen.get_height() - board.height * 32) // 2
        for y in range(board.height):
            for x in range(board.width):
                tile = Game.tiles.get(board.get_cell(x, y))
                if tile:
                    screen.blit(tile, (x0 + x * 32, y0 + y * 32))

        if self.is_level_complete:
            font = pygame.font.SysFont('timesnewroman',  60)
            letter = font.render("Победа!", False, (255, 255, 255), (0, 0, 0))
            x0 = (screen.get_width() - letter.get_width()) // 2
            y0 = (screen.get_height() - letter.get_height()) // 2
            screen.blit(letter, (x0, y0))

        pygame.display.flip()

    def run(self):
        screen = pygame.display.set_mode((640, 480))
        clock = pygame.time.Clock()
        while self.is_game_running:
            self.handle_events(self.board)
            self.update(self.board)
            self.draw(screen, self.board)
            clock.tick(50)

game = Game()
game.run()










