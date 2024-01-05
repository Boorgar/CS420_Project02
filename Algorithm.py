import Agent
import KB

class Solution:
    def __init__(self, room):
        self.room = room
        (x, y) = self.room.get_agent_position()
        self.Agent = Agent.Agent(x, y)
        self.KB = KB.knowledge_base(self.room.get_size())
        self.go_to_door = False
        self.score = 0
        self.map_history = []
        self.score_history = []
    
    def is_valid_move(self, x, y):
        return self.KB.in_board(x, y) and not self.KB.danger(x, y) and not self.KB.in_path(x, y) 
    
    def is_valid_turn(self, x, y):
        return self.KB.in_board(x, y) and not self.KB.in_path(x, y)
    
    def update_perception(self, x, y, for_attack = False):
        if for_attack == True:
            self.KB.kill_Wumpus(x, y)
        else:
            if self.room.is_Treasure(x, y):
                self.score += 1000
                self.score_history.append(self.score)
                self.room.collect_treasure(x, y)
                self.KB.add_action_history("Collect Gold")
                self.map_history.append(self.room.get_map())
            if self.room.is_Empty(x, y):
                self.KB.add_empty(x, y)
            if self.room.is_Breeze(x, y):
                self.KB.add_Pit(x, y)
            if self.room.is_Stench(x, y):
                self.KB.add_Wumpus(x, y)
        
    def move_forward(self, x, y):
        self.Agent.update_position(x, y)
        self.KB.add_path((x, y), False)
        self.KB.add_action("Forward")
        self.score -= 10
        self.score_history.append(self.score)
        self.map_history.append(self.room.get_map())
        self.room.update_agent_position(x, y)
        self.KB.add_action_history("Move Forward")
    
    def turn(self):
        self.Agent.turn_right()
        (x, y) = self.Agent.move_forward()
        if (self.is_valid_move(x, y)):
            self.KB.add_action("Turn Right")
            self.KB.add_action_history("Turn Right")
        else:
            self.Agent.turn_left()
            self.Agent.turn_left()
            self.KB.add_action("Turn Left")
            self.KB.add_action_history("Turn Left")

        self.room.update_agent_face(self.Agent.get_face())

    def turn_without_condition(self):
        self.Agent.turn_right()
        (x, y) = self.Agent.move_forward()
        if self.KB.in_board(x, y):
            self.KB.add_action_history("Turn Right")
        else:
            self.Agent.turn_left()
            self.Agent.turn_left()
            self.KB.add_action_history("Turn Left")

    def end_game(self):
        (x, y) = self.Agent.get_position()
        if self.room.is_Wumpus(x, y) or self.room.is_Pit(x, y):
            self.score -= 10000
            self.score_history.append(self.score)
            return True
        elif self.Agent.get_position() == (0, -1):
            self.score += 10
            self.score_history.append(self.score)
            return True
        else:
            return False


    def get_solution(self):
        while not self.end_game():
            self.score_history.append(self.score)
            self.map_history.append(self.room.get_map())
            (x, y) = self.Agent.get_position()
            self.KB.add_path((x, y), False)
            if len(self.KB.get_path_to_door()) == 0:
                self.Agent.add_queue((x, y), (x, y))
            self.KB.add_action("Start the game")
            while len(self.Agent.get_queue()) != 0 and not self.KB.is_empty_action():
                (x, y) = self.Agent.get_position()

                self.update_perception(x, y)

                if self.KB.can_t_go_further(x, y):
                    if self.KB.can_find_a_way(x, y):
                        (i, j) = self.Agent.move_forward()
                        if self.KB.maybe_a_Wumpus(i, j):
                            self.score -= 100
                            self.score_history.append(self.score)
                            atack_successfully = self.room.Wumpus_take_an_attack(i, j)
                            if atack_successfully:
                                self.KB.add_action_history("Shoot Successfully")
                                self.update_perception(x, y, True)
                                self.map_history.append(self.room.get_map())
                                self.move_forward(i, j)
                                self.map_history.append(self.room.get_map())
                            else:
                                self.KB.add_action_history("Miss")
                                self.turn()
                                self.map_history.append(self.room.get_map())
                        else:
                            self.turn()
                    else:
                        if self.KB.get_previous_action() == "Turn Left":
                            self.KB.back_to_previous_action()
                            self.Agent.turn_right()
                            self.KB.add_action_history("Turn Right")
                        elif self.KB.get_previous_action() == "Turn Right":
                            self.KB.back_to_previous_action()
                            self.Agent.turn_left()
                            self.KB.add_action_history("Turn Left")
                        else:
                            self.KB.back_to_previous_action()
                            parent = self.Agent.back_to_parent()
                            if parent != (-1, -1):
                                self.KB.add_path(parent, True)
                                self.KB.add_stuck(x, y)
                                self.score -= 10
                                self.score_history.append(self.score)
                                (x, y) = self.Agent.get_position()
                                self.room.update_agent_position(x, y)
                                self.map_history.append(self.room.get_map())
                                self.KB.add_action_history("Move Backward")
                            else:
                                self.KB.add_stuck(x, y)
                else:
                    (x, y) = self.Agent.move_forward()
                    if self.is_valid_move(x, y):
                        self.move_forward(x, y)
                    else:
                        self.turn()
            if not self.end_game():
                (x, y) = self.Agent.get_position()
                if self.KB.totally_stuck():
                    if (x, y) == (0, 0):
                        self.turn_without_condition()
                        (x, y) = self.Agent.move_forward()
                        if not self.KB.in_path(x, y):
                            self.move_forward(x, y)
                    elif len(self.KB.get_path_to_door()) > 0 and (x,y) != (0, 0):
                        self.go_to_door = True
                        for i, j in self.KB.get_path_to_door():
                            self.Agent.add_queue(i, j)
                    else:
                        (x, y) = self.Agent.move_forward()
                        if self.KB.in_board(x, y):
                            self.move_forward(x, y)
                        else:
                            self.turn_without_condition()
                elif self.go_to_door == False:
                    self.turn_without_condition()
                    (x, y) = self.Agent.move_forward()
                    if not self.KB.in_path(x, y):
                        self.move_forward(x, y)

        return (self.KB.get_path() , self.score, self.KB.get_action_history(), self.map_history, self.score_history)