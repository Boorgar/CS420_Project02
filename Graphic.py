import sys
import pygame
from Config import *
import Room
from Items import *
import Algorithm

CELL_SIZE = 70
SPACING = 10

def print_board(map, agent_pos):
    for i in range(len(map)):
        for j in range(len(map)):
            if (i, j) == agent_pos:
                print("A", end=" ")
            else:
                print(map[i][j], end=" ")
        print()
    

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
    
    def export_result(self, file_path, history, score):
        try:
            with open(file_path, 'w') as file:
                file.write(str(len(history)) + '\n')
                for action in history:
                    file.write(action + '\n')
                file.write("Final Score: " + str(score) + '\n')
            print(f"Result exported to {file_path}")
        except Exception as e:
            print(f"Error writing to file: {e}")
        
    def draw_score(self):
        text = self.font.render('Score: ' + str(self.score), True, BLACK)
        textRect = text.get_rect()
        textRect.center = (820, 25)
        self.screen.blit(text, textRect)
        pygame.display.update()
         
             
    def final_score(self, score):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (0, 0))
        text = self.victory.render('Your score: ' + str(score), True, BLACK)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.screen.blit(text, textRect)
        pygame.display.update()
        
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
            

    def drawMap(self, map):
        map.reverse()
        self.screen.fill(WHITE)
        
        x = SPACING
        y = SPACING
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if map[i][j] == BREEZE:
                    self.screen.blit(pygame.image.load(IMG_SEEN_CELL), (j * CELL_SIZE, i * CELL_SIZE))
                    text = self.noti.render('Breeze', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
                    self.screen.blit(text, textRect)
                    
                elif STENCH in map[i][j]:
                    self.screen.blit(pygame.transform.scale(pygame.image.load(IMG_SEEN_CELL), (CELL_SIZE, CELL_SIZE)), (j * CELL_SIZE, i * CELL_SIZE))
                    text = self.noti.render('Stench', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
                    self.screen.blit(text, textRect)
                    
                    
                elif PIT in map[i][j]:
                    self.screen.blit(pygame.image.load(IMG_PIT), (j * CELL_SIZE, i * CELL_SIZE))
                elif WUMPUS in map[i][j]:
                    self.screen.blit(pygame.transform.scale(pygame.image.load(IMG_WUMPUS), (CELL_SIZE, CELL_SIZE)), (j * CELL_SIZE, i * CELL_SIZE))
                elif GOLD in map[i][j]:
                    self.screen.blit(pygame.transform.scale(pygame.image.load(IMG_GOLD), (CELL_SIZE, CELL_SIZE)), (j * CELL_SIZE, i * CELL_SIZE))
                    
                elif AGENT in map[i][j]:
                    self.screen.blit(pygame.transform.scale(pygame.image.load(IMG_HUNTER_RIGHT), (CELL_SIZE, CELL_SIZE)), (j * CELL_SIZE, i * CELL_SIZE))
                else:
                    self.screen.blit(pygame.image.load(IMG_INITIAL_CELL), (j * CELL_SIZE, i * CELL_SIZE))
                                    
               
               
    def run(self):
        
        
        
        while True:

            # Each if statement is a state of the game
            if self.state == MENU:
                self.menu_draw()

            if self.state == RUNNING:
                
                if self.map_i == 1:
                    self.room = Room.room(MAP_LIST[0])
                elif self.map_i == 2:
                    self.room = Room.room(MAP_LIST[1])
                elif self.map_i == 3:
                    self.room = Room.room(MAP_LIST[2])
                elif self.map_i == 4:
                    self.room = Room.room(MAP_LIST[3])
                elif self.map_i == 5:
                    self.room = Room.room(MAP_LIST[4])
                    
                agent_path, score, action_history, map_history, score_history = Algorithm.Solution(self.room).get_solution()

                self.export_result(OUTPUT_LIST[self.map_i - 1], action_history, score)
                
                file_path = MAP_LIST[self.map_i - 1]
                with open(file_path, 'r') as file:
                        size = int(file.readline().strip())
                        global BOARD_SIZE
                        BOARD_SIZE = size

                        self.world_map = []
                        for _ in range(size):
                            line = file.readline().strip()
                            room_contents = line.split('.')
                            self.world_map.append(room_contents)
                
                
                tmp_pit = []
                tmp_wumpus = []
                for i in range(len(self.world_map)):
                    for j in range(len(self.world_map)):
                        if "P" in self.world_map[i][j]:
                            tmp_pit.append((i, j))
                        if "W" in self.world_map[i][j]:
                            tmp_wumpus.append((i, j))
                        if "A" in self.world_map[i][j] :
                            self.world_map[i][j].replace("A", "-")
                            agent_x = j
                            agent_y = i
                
                
                self.map = GameMap((agent_x, agent_y))
                self.arrow = Arrow()
                self.gold = Gold_Manager()
                
                
                self.agent = Agent(agent_x, agent_y)
                self.agent.load_image()
                self.all_sprites = pygame.sprite.Group()
                self.all_sprites.add(self.agent)
                
                
                # Create pit and wumpus objects                
                self.pit = Pit_Manager(tmp_pit)
                self.wumpus = Wumpus_Manager(tmp_wumpus)
            
                self.screen.fill(WHITE)
                self.screen.blit(self.bg, (0, 0))
                pygame.time.delay(100)
                
                
                # for action in action_history:
                    
                #     print(action)
                #     self.display_action(action)
                #     agent_x, agent_y = self.agent.get_pos()
                    
                #     print(agent_x, agent_y)
                #     print_board(self.world_map, (agent_y, agent_x))
                    
                #     pygame.time.delay(10)
                
                # for path in agent_path:
                #     print(path)
                #     self.drawMap(self.world_map)
                #     # draw agent at path pos
                #     x, y = path
                #     self.screen.blit(pygame.image.load(IMG_HUNTER_RIGHT), (x * CELL_SIZE, y * CELL_SIZE))
                    
                    
                #     print_board(self.world_map, path)
                    
                #     pygame.display.update()
                #     pygame.time.delay(50)
                
                
                i_counter = 1
                j_counter = 0
                for cave_map in map_history:
                    # Check if last cave map
                    if cave_map == map_history[-1]:
                        pygame.time.delay(100)
                        break
                        
                    tmp_action = action_history[j_counter]
                    
                    
                    # Exhaust all the turning
                    while tmp_action == "Turn Right" or tmp_action == "Turn Left":
                        if j_counter < len(action_history) - 1:
                            j_counter += 1
                        tmp_action = action_history[j_counter]
                        if tmp_action == "Turn Right":
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
                            pygame.display.update()
                            
                        if tmp_action == "Turn Left":
                            if self.direct == 0:
                                self.direct = self.agent.turn_left()
                            if self.direct == 1:
                                self.direct = self.agent.turn_right()
                            if self.direct == 2:
                                self.direct = self.agent.turn_down()
                            if self.direct == 3:
                                self.direct = self.agent.turn_up()
                            self.all_sprites.update()
                            self.draw_score()
                            self.all_sprites.draw(self.screen)
                            pygame.display.update()
                    

                    
                    if tmp_action == "Move Forward":
                        text = self.font.render('Agent Move Forward', True, BLACK)
                        textRect = text.get_rect()
                        textRect.center = (820, 100)
                        self.screen.blit(text, textRect)
                        pygame.display.update()
                        if j_counter < len(action_history) - 1:
                            j_counter += 1
                        
                    elif tmp_action == "Move Backward":
                        text = self.font.render('Agent Move Backward', True, BLACK)
                        textRect = text.get_rect()
                        textRect.center = (820, 100)
                        self.screen.blit(text, textRect)
                        pygame.display.update()
                        if j_counter < len(action_history) - 1:
                            j_counter += 1
                        
                    elif tmp_action == "Shoot Successfully":
                        text = self.font.render('Agent Shoot Successfully', True, BLACK)
                        textRect = text.get_rect()
                        textRect.center = (820, 100)
                        self.screen.blit(text, textRect)
                        pygame.display.update()
                        
                        if self.direct == 0:
                            j -= 1
                        elif self.direct == 1:
                            j += 1
                        elif self.direct == 2:
                            i -= 1
                        elif self.direct == 3:
                            i += 1
                            
                        self.arrow.shoot(self.direct, self.screen, i, j)
                        if j_counter < len(action_history) - 1:
                            j_counter += 1                       
                    else:
                        if j_counter < len(action_history) - 1:
                            j_counter += 1
                        pass    
                    
                    
                    self.score = score_history[i_counter]
                    if i_counter < len(score_history) - 1:
                        i_counter += 1
                    self.draw_score()
                    # print(cave_map)
                    self.drawMap(cave_map)
                    pygame.display.update()
                    pygame.time.delay(10)
                    
                    
                    
                print("Action history", action_history)
                print("Score", score)
                self.final_score(score)
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
            x, y = self.agent.get_pos()
            self.gold.gold_collected(self.screen, self.font, (x,y))
            
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
                j -= 1
            elif self.direct == 1:
                j += 1
            elif self.direct == 2:
                i -= 1
            elif self.direct == 3:
                i += 1
            
            
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