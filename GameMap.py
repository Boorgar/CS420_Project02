import pygame
from Config import *

class GameMap:
    def __init__(self, init_agent_pos):
        self.spacing = 10
        self.boardSize = 10
        
        # Pygame Operations
        self.cell_size = 60

        # Load images for celss with pygame
        self.cell = pygame.image.load(IMG_INITIAL_CELL).convert()
        self.discovered_cell = pygame.image.load(IMG_SEEN_CELL).convert()
        self.pit = pygame.image.load(IMG_PIT).convert()

        # Marking discovered pits
        self.pit_discover = [[False for i in range(self.boardSize)] for j in range(self.boardSize)]
        
        # Marking discovered cells
        self.is_discovered = [[False for i in range(self.boardSize)] for j in range(self.boardSize)]
        # Marking initial agent cell as discovered
        self.is_discovered[init_agent_pos[0] - 1][init_agent_pos[1] - 1] = True 

    def draw(self, screen):
        x = self.spacing
        y = self.spacing

        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if(self.is_discovered[i][j]):
                    screen.blit(self.discovered_cell, (x, y))
                elif not self.is_discovered[i][j]:
                    if self.pit_discover[i][j]:
                        screen.blit(self.pit, (x, y))
                    else:
                        screen.blit(self.cell, (x, y))
            x += self.spacing + self.cell_size
            y += self.spacing + self.cell_size
            x = self.spacing

    def discover_cell(self, pos: tuple):
        i, j = pos
        self.is_discovered[i][j] = True

    def discovered(self):
        return self.is_discovered

    def agent_climb(self, screen, font):
        text = font.render('Climbed out!!!', True, BLACK)
        textRect = text.get_rect()
        textRect.center = (830, 100)
        screen.blit(text, textRect)
        text = font.render('Score + 10', True, BLACK)
        textRect.center = (850, 150)
        screen.blit(text, textRect)

    def pit_detect(self, i, j):
        self.pit_discover[i][j] = True

