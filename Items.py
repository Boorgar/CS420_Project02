import pygame
from Config import *

class GameMap:
    def __init__(self, init_agent_pos):
        self.spacing = 10
        self.cell_size = 60
        self.cell = pygame.image.load(IMG_INITIAL_CELL).convert()
        self.pit = pygame.image.load(IMG_PIT).convert()
        self.cell_seen = pygame.image.load(IMG_SEEN_CELL).convert()
        
        self.size = BOARD_SIZE
        self.pit_discovered = [[False for i in range(self.size)] for j in range(self.size)]
        self.cell_discovered = [[False for i in range(self.size)] for j in range(self.size)]
       
        # Agent discover the initial cell
        self.cell_discovered[init_agent_pos[1]][init_agent_pos[0]] = True

    def draw(self, screen):
        x = self.spacing
        y = self.spacing

        for i in range(0, self.size):
            for j in range(0, self.size):
                if(self.cell_discovered[i][j]):
                    screen.blit(self.cell_seen, (x, y))
                    x += self.spacing + self.cell_size
                elif not self.cell_discovered[i][j]:
                    if self.pit_discovered[i][j]:
                        screen.blit(self.pit, (x, y))
                        x += self.spacing + self.cell_size
                    else:
                        screen.blit(self.cell, (x, y))
                        x += self.spacing + self.cell_size
            y += self.spacing + self.cell_size
            x = self.spacing

    def discover_cell(self, pos):
        x, y = pos
        self.cell_discovered[y][x] = True

    def get_discovered(self):
        return self.cell_discovered

    def agent_climb(self, screen, font):    
        text = font.render('Agent climbed out!!!', True, BLACK)
        textRect = text.get_rect()
        textRect.center = (830, 100)
        screen.blit(text, textRect)
        text = font.render('Score +10', True, BLACK)
        textRect.center = (850, 150)
        screen.blit(text, textRect)

    def discover_pit(self, pit_pos):
        x, y = pit_pos
        self.pit_discovered[y][x] = True
        
    def read_map(self, map):
        for i in range(0, self.size):
            for j in range(0, self.size):
                
                # When read new state, check if the cell is discovered
                
                if not self.pit_discovered[i][j]:
                    self.pit_discovered[i][j] = True
                if not self.cell_discovered[i][j]:
                    self.cell_discovered[i][j] = True
                    
        
class Pit_Manager:
    def __init__(self, pit_pos_list):
        self.image = pygame.image.load(IMG_PIT).convert()
        self.image = pygame.transform.scale(self.image, (100, 200))
        
        self.is_discovered = None
        self.size = BOARD_SIZE
        
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        self.pit_pos = [[False for i in range(self.size)] for j in range(self.size)]
        
        for i in range(len(pit_pos_list)):
            x, y = pit_pos_list[i]
            self.pit_pos[x][y] = True

        for i in range(self.size):
            for j in range(self.size):
                if self.pit_pos[i][j]:
                    if i > 0:
                        self.noti[i - 1][j] = True
                    if i < self.size - 1:
                        self.noti[i + 1][j] = True
                    if j > 0:
                        self.noti[i][j - 1] = True
                    if j < self.size - 1:
                        self.noti[i][j + 1] = True

    def update(self, screen, font, is_discovered):
        for i in range(self.size):
            for j in range (self.size):
                if self.noti[i][j] and is_discovered[i][j]:
                    text = font.render('Breeze', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (42 + j * 70, 40 + i * 70)
                    screen.blit(text, textRect)
                    pygame.display.update()
                    
    def pit_discovered(self):
        self.is_discovered = True
        
    def pit_i_j(self, i, j):
        return self.noti[i][j]

# Manage all wumpus, assume pos_list is a list of tuples
class Wumpus_Manager:
    def __init__(self, wumpus_pos_list):
        self.image = pygame.image.load(IMG_WUMPUS).convert()
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.size = BOARD_SIZE
        
        self.pos = (835, 100)
        
        # Create a 2D array to store the discovered status of wumpus
        self.is_discovered = None
        
        # Create a 2D array to store the stench of wumpus
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        # Create a 2D array to store the position of wumpus
        self.wumpus_pos = [[False for i in range(self.size)] for j in range(self.size)]
    
        # Get the position of wumpus from the list of tuples
        for i in range(len(wumpus_pos_list)):
            x, y = wumpus_pos_list[i]
            self.wumpus_pos[x][y] = True
            
        for i in range(self.size):
            for j in range(self.size):
                if self.wumpus_pos[i][j]:
                    if i > 0:
                        self.noti[i - 1][j] = True
                    if i < self.size - 1:
                        self.noti[i + 1][j] = True
                    if j > 0:
                        self.noti[i][j - 1] = True
                    if j < self.size - 1:
                        self.noti[i][j + 1] = True

    def wumpus_show_kill(self, screen, font):
        text = font.render('Killed Wumpus!!!', True, BLACK)
        textRect = text.get_rect()
        textRect.center = self.pos
        screen.blit(text, textRect)
        screen.blit(self.image, (800, 200))
        pygame.display.update()


    def wumpus_killed(self, i, j):
        self.wumpus_pos[i][j] = False
        if i > 0:
            self.noti[i-1][j] = False
        if i < self.size - 1:
            self.noti[i+1][j] = False
        if j > 0:
            self.noti[i][j - 1] = False
        if j < self.size - 1:
            self.noti[i][j + 1] = False
            
    def wumpus_missed(self, screen, font):
        text = font.render('Missed!!!', True, BLACK)
        textRect = text.get_rect()
        textRect.center = self.pos
        screen.blit(text, textRect)
        pygame.display.update()

    def update(self, screen, font, is_discovered):
        for i in range(self.size):
            for j in range (self.size):
                if self.noti[i][j] and is_discovered[i][j]:
                    text = font.render('Stench!', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (45 + j * 70, 30 + i * 70)
                    screen.blit(text, textRect)
                    pygame.display.update()

    def stench_i_j(self, i, j):
        return self.noti[i][j]


class Gold:
    def __init__(self):
        self.image = pygame.image.load(IMG_GOLD).convert()
        self.image = pygame.transform.scale(self.image, (150,300))
        self.text_pos = (835, 100)

    def gold_collected(self, screen, font):
        text = font.render('Agent found a gold pile!!!', True, BLACK)
        textRect = text.get_rect()
        textRect.center = self.text_pos
        screen.blit(text, textRect)
        screen.blit(self.image, (750, 200))
        text = font.render('Score +1000', True, BLACK)
        textRect.center = (900, 600)
        screen.blit(text, textRect)
        pygame.display.update()


class Arrow:
    def __init__(self):
        self.img_list = []
        img_list = [IMG_ARROW_RIGHT, IMG_ARROW_LEFT, IMG_ARROW_UP, IMG_ARROW_DOWN]
        for i in range(0, 4):
            img = pygame.image.load(img_list[i]).convert()
            self.img_list.append(img)

    def shoot(self, direction:str, screen, pos_x, pos_y):
        if direction == 'up':
            self.shoot_up(screen, pos_x, pos_y)
        elif direction == 'down':
            self.shoot_down(screen, pos_x, pos_y)
        elif direction == 'left':
            self.shoot_left(screen, pos_x, pos_y)
        elif direction == 'right':
            self.shoot_right(screen, pos_x, pos_y)
            
    def shoot_up(self, screen, x, y):
        x = 10 + x * 70
        y = 10 + (y - 1) * 70
        screen.blit(self.img_list[2], (x, y))
        pygame.display.update()

    def shoot_down(self, screen, x, y):
        i = 10 + x * 70
        j = 10 + (y + 1) * 70
        screen.blit(self.img_list[3], (i, j))
        pygame.display.update()

    def shoot_right(self, screen, x, y):
        x = 10 + (x + 1) * 70
        y = 10 + y * 70
        screen.blit(self.img_list[0], (x, y))
        pygame.display.update()

    def shoot_left(self, screen, x, y):
        x = 10 + (x - 1) * 70
        y = 10 + y * 70
        screen.blit(self.img_list[1], (x, y))
        pygame.display.update()


class Agent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.image = pygame.image.load(IMG_HUNTER_RIGHT).convert()
        self.img_list = []
        self.y = 40 + (x - 1) * 70
        self.x = 40 + (y - 1) * 70
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.spacing = 70
        self.i = x
        self.j = y
        
    def load_image(self):
        self.img_list.append(self.image)
        temp = [IMG_HUNTER_LEFT, IMG_HUNTER_UP, IMG_HUNTER_DOWN]
        for i in range (0, 3):
            img = pygame.image.load(temp[i]).convert()
            self.img_list.append(img)

    def appear(self, screen):
        screen.blit(self.image, (self.x - 30, self.y - 30))

    def get_score(self):
        return self.score
    
    def turn_up(self):
        self.image = self.img_list[3]
        return 0

    def turn_down(self):
        self.image = self.img_list[2]
        return 1

    def turn_left(self):
        self.image = self.img_list[1]
        return 2

    def turn_right(self):
        self.image = self.img_list[0]
        return 3
    
    def move_forward(self, direct):
        if direct == 0:
            self.move_up()
        elif direct == 1:
            self.move_down()
        elif direct == 2:
            self.move_left()
        elif direct == 3:
            self.move_right()
            
    def move_backward(self, direct):
        if direct == 0:
            self.move_down()
        elif direct == 1:
            self.move_up()
        elif direct == 2:
            self.move_right()
        elif direct == 3:
            self.move_left()

    def move_up(self):
        self.y -= self.spacing
        self.score -= 10
        if self.j > 0:
            self.j -= 1

    def move_down(self):
        self.y += self.spacing
        self.score -= 10
        if self.j < 9:
            self.j += 1

    def move_left(self):
        self.x -= self.spacing
        self.score -= 10
        if self.i > 0:
            self.i -= 1

    def move_right(self):
        self.x += self.spacing
        self.score -= 10
        if self.i < 9:
            self.i += 1
            
    def update(self):
        if self.x > 670:
            self.x -= self.spacing
            self.score += 10

        elif self.x < 40:
            self.x += self.spacing
            self.score += 10

        elif self.y < 40:
            self.y += self.spacing
            self.score += 10

        elif self.y > 670:
            self.y -= self.spacing
            self.score += 10

        self.rect.center = (self.x, self.y)
        
    def get_pos(self):
        return self.i, self.j

    def shoot(self):
        self.score -= 100

    def wumpus_or_pit_collision(self):
        self.score -= 10000

    def grab_gold(self):
        self.score += 100

    def climb(self):
        self.score += 10

    def move_to(self, pos):
        x, y = pos
        self.x = 40 + (y - 1) * 70
        self.y = 40 + (x - 1) * 70
        self.rect.center = (self.x, self.y)
        self.i = x - 1
        self.j = y - 1