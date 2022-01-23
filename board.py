import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.left = 10
        self.top = 10
        self.cell_size = 30

        self.board = [[0] * self.width for i in range(self.height)]
        self.colors = [(0, 0, 0),  # пусто
                       (255, 255, 255), # стена
                       (200, 200, 200), # кот
                       (255, 0, 0), # ебака
                       (0, 255, 0), # хозяйка
                       (0, 0, 255)] # труп

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                color = self.colors[self.board[i][j]]
                
                par = (self.left + j * self.cell_size,
                         self.top + i * self.cell_size,
                         self.cell_size, self.cell_size)
                
                pygame.draw.rect(screen, color, par, 0)
                pygame.draw.rect(screen, (255, 255, 255), par, 1)
