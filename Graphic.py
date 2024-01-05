import sys
import pygame
from Config import *
import Room
from Items import *
import Algorithm

CELL_SIZE = 70
SPACING = 10

class Graphic:
    def __init__(self):
        # Init Pygame Assets
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.caption = pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(FONT, 30)
        self.noti = pygame.font.Font(FONT, 15)
        self.victory = pygame.font.Font(FONT, 50)
        self.all_sprites = pygame.sprite.Group()

        self.map = None
        self.agent = None
        self.gold = None
        self.wumpus = None
        self.pit = None
        self.arrow = None
        

        self.state = MENU
        self.map_i = 1
        self.mouse = None

        # Background image
        self.bg = pygame.image.load('./Assets/Images/cave_background.png').convert()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.direct = 3
             
        
        
    def draw_score(self):
        self.screen.fill(WHITE)
        self.map.draw(self.screen)
        # text = self.font.render('Your score: ' + str(score_history), True, BLACK)
        # textRect = text.get_rect()
        # textRect.center = (820, 25)
        # self.screen.blit(text, textRect)

    def draw_button(self, surf, rect, button_color, text_color, text):
        pygame.draw.rect(surf, button_color, rect)
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    def menu_draw(self):
        # Draw background image
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (0, 0))
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Use hardcoded mouse position to determine which button is clicked
                if 235 <= self.mouse[0] <= 735 and 120 <= self.mouse[1] <= 170:
                    self.state = RUNNING
                    self.map_i = 1
                elif 235 <= self.mouse[0] <= 735 and 200 <= self.mouse[1] <= 250:
                    self.state = RUNNING
                    self.map_i = 2
                elif 235 <= self.mouse[0] <= 735 and 280 <= self.mouse[1] <= 330:
                    self.state = RUNNING
                    self.map_i = 3
                elif 235 <= self.mouse[0] <= 735 and 360 <= self.mouse[1] <= 410:
                    self.state = RUNNING
                    self.map_i = 4
                elif 235 <= self.mouse[0] <= 735 and 440 <= self.mouse[1] <= 490:
                    self.state = RUNNING
                    self.map_i = 5
                elif 235 <= self.mouse[0] <= 735 and 520 <= self.mouse[1] <= 570:
                    pygame.quit()
                    sys.exit()

        # Highlight button when mouse is hovering over it
        self.mouse = pygame.mouse.get_pos()
        if 235 <= self.mouse[0] <= 735 and 120 <= self.mouse[1] <= 170:
            self.draw_button(self.screen, TEXT_1_POS, DARK_GREY, RED, "TEST 1")
        else:
            self.draw_button(self.screen, TEXT_1_POS, LIGHT_GREY, BLACK, "TEST 1")
        if 235 <= self.mouse[0] <= 735 and 200 <= self.mouse[1] <= 250:
            self.draw_button(self.screen, TEXT_2_POS, DARK_GREY, RED, "TEST 2")
        else:
            self.draw_button(self.screen, TEXT_2_POS, LIGHT_GREY, BLACK, "TEST 2")
        if 235 <= self.mouse[0] <= 735 and 280 <= self.mouse[1] <= 330:
            self.draw_button(self.screen, TEXT_3_POS, DARK_GREY, RED, "TEST 3")
        else:
            self.draw_button(self.screen, TEXT_3_POS, LIGHT_GREY, BLACK, "TEST 3")
        if 235 <= self.mouse[0] <= 735 and 360 <= self.mouse[1] <= 410:
            self.draw_button(self.screen, TEXT_4_POS, DARK_GREY, RED, "TEST 4")
        else:
            self.draw_button(self.screen, TEXT_4_POS, LIGHT_GREY, BLACK, "TEST 4")
        if 235 <= self.mouse[0] <= 735 and 440 <= self.mouse[1] <= 490:
            self.draw_button(self.screen, TEXT_5_POS, DARK_GREY, RED, "TEST 5")
        else:
            self.draw_button(self.screen, TEXT_5_POS, LIGHT_GREY, BLACK, "TEST 5")
        if 235 <= self.mouse[0] <= 735 and 520 <= self.mouse[1] <= 570:
            self.draw_button(self.screen, EXIT_POS, DARK_GREY, RED, "EXIT")
        else:
            self.draw_button(self.screen, EXIT_POS, LIGHT_GREY, BLACK, "EXIT")
        pygame.display.update()
            

    def win_draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (0, 0))

        if self.state == WIN:
            text = self.victory.render('VICTORY!!!', True, BLACK)
        elif self.state == TRYBEST:
            text = self.victory.render('TRY BEST!!!', True, BLACK)

        textRect = text.get_rect()
        textRect.center = (500, 50)
        self.screen.blit(text, textRect)
        score = self.agent.get_score()
        text = self.victory.render('Your score: ' + str(score), True, BLACK)
        textRect.center = (450, 100)
        self.screen.blit(text, textRect)

    def win_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        pygame.time.delay(200)
        self.state = MENU

    def drawMap(self, map):
        
        self.screen.fill(WHITE)
        
        x = SPACING
        y = SPACING
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if map[i][j] == BREEZE:
                    self.screen.blit(pygame.image.load(IMG_SEEN_CELL), (j * CELL_SIZE, i * CELL_SIZE))
                    text = self.font.render('Breeze', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (x + 20, y + 20)
                    self.screen.blit(text, textRect)
                    
                elif map[i][j] == STENCH:
                    self.screen.blit(pygame.transform.scale(pygame.image.load(IMG_SEEN_CELL), (CELL_SIZE, CELL_SIZE)), (j * CELL_SIZE, i * CELL_SIZE))
                    text = self.font.render('Stench', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (x + 20, y + 20)
                    
                elif map[i][j] == PIT:
                    self.screen.blit(pygame.image.load(IMG_PIT), (j * CELL_SIZE, i * CELL_SIZE))
                elif map[i][j] == WUMPUS:
                    self.screen.blit(pygame.transform.scale(pygame.image.load(IMG_WUMPUS), (CELL_SIZE, CELL_SIZE)), (j * CELL_SIZE, i * CELL_SIZE))
                elif map[i][j] == GOLD:
                    self.screen.blit(pygame.transform.scale(pygame.image.load(IMG_GOLD), (CELL_SIZE, CELL_SIZE)), (j * CELL_SIZE, i * CELL_SIZE))
                
               
               
    def run(self):
        while True:

            # Each if statement is a state of the game
            if self.state == MENU:
                self.menu_draw()

            if self.state == RUNNING:
                # if self.map_i == 1:
                #     self.room = Room.room(MAP_LIST[0])
                # elif self.map_i == 2:
                #     self.room = Room.room(MAP_LIST[1])
                # elif self.map_i == 3:
                #     self.room = Room.room(MAP_LIST[2])
                # elif self.map_i == 4:
                #     self.room = Room.room(MAP_LIST[3])
                # elif self.map_i == 5:
                #     self.room = Room.room(MAP_LIST[4])
                    
                self.room = Room.room("test.txt")
                
                
                agent_path, score, action_history, map_history, score_history = Algorithm.Solution(self.room).get_solution()
                # Get agent initial position

                file_path = "test.txt"
                with open(file_path, 'r') as file:
                    size = int(file.readline().strip())

                    self.world_map = []
                    for _ in range(size):
                        line = file.readline().strip()
                        room_contents = line.split('.')
                        self.world_map.append(room_contents)
                self.world_map.reverse()
                
                # tmp_pit = []
                # tmp_wumpus = []
                # for i in range(size):
                #     for j in range(size):
                #         if 'P' in self.world_map[i][j]:
                #             tmp_pit.append((i, j))
                #         if 'W' in self.world_map[i][j]:
                #             tmp_wumpus.append((i, j))
                #         if 'A' in self.world_map[i][j]:
                #             agent_x = i
                #             agent_y = j
                
                

                
                
                # self.map = GameMap((agent_x, agent_y))
                # self.arrow = Arrow()
                # self.gold = Gold()
                
                
                # self.agent = Agent(agent_x, agent_y)
                # self.agent.load_image()
                # self.all_sprites = pygame.sprite.Group()
                # self.all_sprites.add(self.agent)
                
                
                # # Iterate through room.map to get all pits and wumpus
                # for i in range(self.room.size):
                #     for j in range(self.room.size):
                #         if self.room.is_Pit(i, j):
                #             tmp_pit.append((i, j))
                #         if self.room.is_Wumpus(i, j):
                #             tmp_wumpus.append((i, j))
                
                # Create pit and wumpus objects
                # self.pit = Pit_Manager(tmp_pit)
                # self.wumpus = Wumpus_Manager(tmp_wumpus)
            
                
                # self.draw_score()
                # pygame.time.delay(100)
                
                # for action in action_history:
                    
                #     print(action)
                #     self.display_action(action)
                #     agent_x, agent_y = self.agent.get_pos()
                #     pygame.time.delay(100)
                
                for path in agent_path:
                    print(path)
                    self.drawMap(self.world_map)
                    # draw agent at path pos
                    x, y = path
                    self.screen.blit(pygame.image.load(IMG_HUNTER_RIGHT), (x * CELL_SIZE, y * CELL_SIZE))
                    pygame.display.update()
                    pygame.time.delay(100)
                    
                    
                self.state = WIN
            if self.state == WIN:
                self.state = MENU
            self.clock.tick(60)
                
                    
                    
                    
                    
                    
    def display_action(self, action):
        if action == "Move Forward":
            self.agent.move_forward(self.direct)
            i, j = self.agent.get_pos()
            self.map.discover_cell((i, j))
            self.all_sprites.update()
            self.draw_score()
            self.all_sprites.draw(self.screen)
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == "Move Backward":
            self.agent.move_backward(self.direct)
            i, j = self.agent.get_pos()
            self.map.discover_cell((i, j))
            self.all_sprites.update()
            self.draw_score()
            self.all_sprites.draw(self.screen)
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == "Turn Right":
            if self.direct == 0:
                self.direct = self.agent.turn_right()
            if self.direct == 1:
                self.direct = self.agent.turn_left()
            if self.direct == 2:
                self.direct = self.agent.turn_up()
            if self.direct == 3:
                self.direct = self.agent.turn_down()
            self.all_sprites.update()
            self.draw_score()
            self.all_sprites.draw(self.screen)
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == "Turn Left":
            if self.direct == 0:
                self.direct = self.agent.turn_left()
            if self.direct == 1:
                self.direct = self.agent.turn_right()
            if self.direct == 2:
                self.direct = self.agent.turn_down()
            if self.direct == 3:
                self.direct = self.agent.turn_up()
            
            self.direct = self.agent.turn_left()
            self.all_sprites.update()
            self.draw_score()
            self.all_sprites.draw(self.screen)
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == "Collect Gold":
            self.agent.grab_gold()
            self.all_sprites.update()
            self.draw_score()
            self.all_sprites.draw(self.screen)
            self.gold.gold_collected(self.screen, self.font)
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == "Shoot Successfully":
            self.agent.shoot()
            self.all_sprites.update()
            self.draw_score()   
            self.all_sprites.draw(self.screen)
            i, j = self.agent.get_pos()
            self.arrow.shoot(self.direct, self.screen, i, j)
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            
            if self.direct == 0:
                i -= 1
            elif self.direct == 1:
                i += 1
            elif self.direct == 2:
                j -= 1
            elif self.direct == 3:
                j += 1
            
            
            self.wumpus.wumpus_killed(i, j)
            self.wumpus.wumpus_show_kill(self.screen, self.font)
            
            i, j = self.agent.get_pos()
            
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            
        elif action == "Miss":
            self.agent.shoot()
            self.all_sprites.update() 
            self.draw_score()  
            self.all_sprites.draw(self.screen)
            i, j = self.agent.get_pos()
            self.arrow.shoot(self.direct, self.screen, i, j)
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            
            self.wumpus.wumpus_missed(self.screen, self.font)
            
            i, j = self.agent.get_pos()
            
            temp = self.map.get_discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            


if __name__ == '__main__':
    graphic = Graphic()

    graphic.run()