import pygame
import math
from queue import PriorityQueue

WIDTH = 1600
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm Visualizer")

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 128, 0)
LIGHT_BLUE = (64, 255, 200)

def main(window, width):
    ROWS = 100
    grid = create_grid(ROWS, width)

    begin = None
    fin = None
    
    running = True

    while running:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #check left mouse clicked
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(mouse_pos, ROWS, width)
                Square = grid[row][col]
                if not begin and Square != fin:
                    begin = Square
                    begin.make_begin()

                elif not fin and Square != begin:
                    fin = Square
                    fin.make_fin()
                
                elif Square != fin and Square != begin:
                    Square.make_obst()
            #check right mouse clicked
            elif pygame.mouse.get_pressed()[2]:
                mouse_pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(mouse_pos, ROWS, width)
                Square = grid[row][col]
                Square.reset()
                if Square == begin:
                    begin = None
                elif Square == fin:
                    fin = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and begin and fin:
                    for row in grid:
                        for Square in row:
                            Square.add_near(grid)
                    algorithm(lambda: draw(window, grid, ROWS, width), grid, begin, fin)
            
                if event.key == pygame.K_ESCAPE:
                    begin = None
                    fin = None
                    grid = create_grid(ROWS, width)

    pygame.quit()
class Square:
    def __init__(self, row, col, width, rows_max):
        self.col = col
        self.row = row
        self.y = col * width
        self.x = row * width
        self.near = []
        self.color = WHITE
        self.rows_max = rows_max
        self.width = width

    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN

    def is_obst(self):
        return self.color == BLACK

    def is_begin(self):
        return self.color == BLUE

    def is_fin(self):
        return self.color == PURPLE

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = WHITE
    
    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_obst(self):
        self.color = BLACK

    def make_begin(self):
        self.color = BLUE

    def make_fin(self):
        self.color = PURPLE
    
    def make_path(self):
        self.color = YELLOW

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def add_near(self, grid):
        self.near = []
        #Down
        if self.row < self.rows_max - 1 and not grid[self.row + 1][self.col].is_obst():
            self.near.append(grid[self.row + 1][self.col])
        #Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_obst():
            self.near.append(grid[self.row - 1][self.col])
        #Right
        if self.col < self.rows_max - 1 and not grid[self.row][self.col + 1].is_obst():
            self.near.append(grid[self.row][self.col + 1])
        #Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_obst():
            self.near.append(grid[self.row][self.col - 1])
        #Down_Left
        if self.row < self.rows_max - 1 and self.col > 0 and not grid[self.row + 1][self.col-1].is_obst() and not (grid[self.row + 1][self.col].is_obst() or grid[self.row][self.col - 1].is_obst()):
            self.near.append(grid[self.row + 1][self.col-1])
        #Down_Right
        if self.row < self.rows_max - 1 and self.col < self.rows_max - 1 and not grid[self.row + 1][self.col+1].is_obst() and not (grid[self.row + 1][self.col].is_obst() or grid[self.row][self.col + 1].is_obst()):
            self.near.append(grid[self.row + 1][self.col+1])
        #Up_Left
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_obst() and not (grid[self.row][self.col - 1].is_obst() or grid[self.row - 1][self.col].is_obst()):
            self.near.append(grid[self.row - 1][self.col-1])
        #Up_Right
        if self.row > 0 and self.col < self.rows_max - 1 and not grid[self.row - 1][self.col + 1].is_obst() and not (grid[self.row - 1][self.col].is_obst() or grid[self.row][self.col + 1].is_obst()):
            self.near.append(grid[self.row - 1][self.col+1])
    def __lt__(self, other):
        return False

def hFun(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return abs(x1 - x2) + abs(y1 - y2)

def create_grid(row, width):
    grid = []
    gap = width // row
    for i in range(row):
        grid.append([])
        for j in range(row):
            square = Square(i, j, gap, row)
            grid[i].append(square)
    return grid

def draw_grid(window, row, width):
    gap = width // row
    for i in range(row):
        pygame.draw.line(window, GRAY, (0, i * gap), (width, i * gap))
    for j in range(row):
        pygame.draw.line(window, GRAY, (j * gap, 0), (j * gap, width))

def draw(window, grid, row, width):
    window.fill(WHITE)

    for row in grid:
        for Square in row:
            Square.draw(window)

    draw_grid(window, 100, 1600)
    pygame.display.update()

def get_clicked_pos(pos, row, width):
    gap = width // row
    x, y = pos
    col = x // gap
    row = y // gap

    return row, col

def algorithm(draw, grid, begin, fin):
    count = 0
    open_squares = PriorityQueue()
    open_squares.put((0, count, begin))
    where_parent = {}
    score_g = {Square: float("inf") for row in grid for Square in row}
    score_g[begin] = 0
    score_f = {Square: float("inf") for row in grid for Square in row}
    score_f[begin] = hFun(begin.get_pos(), fin.get_pos())

    open_squares_hash = {begin}

    while not open_squares.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_squares.get()[2]
        open_squares_hash.remove(current)

        if current == fin:
            #draw path
            draw_path(where_parent, fin, draw)
            fin.make_fin()
            begin.make_begin()
            return True
        for near in current.near:
            temp_score_g = score_g[current] + 1

            if temp_score_g < score_g[near]:
                where_parent[near] = current
                score_g[near] = temp_score_g
                score_f[near] = temp_score_g + hFun(near.get_pos(), fin.get_pos())

                if near not in open_squares_hash:
                    count += 1
                    open_squares.put((score_f[near], count, near))
                    open_squares_hash.add(near)
                    near.make_open()
        draw()

        if current != begin:
            current.make_closed()
    return False

def draw_path(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()


main(WINDOW, WIDTH)