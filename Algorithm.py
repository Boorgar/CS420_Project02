import Agent
import KB

class Solution:
    def __init__(self, room):
        self.room = room
        (x, y) = self.room.get_agent_position()
        self.Agent = Agent.Agent(x, y)
        self.KB = KB.knowledge_base(self.room.get_size())
        self.score = 0
    
    def is_valid_move(self, x, y):
        return self.KB.in_board(x, y) and not self.KB.danger(x, y) and not self.KB.in_path(x, y)
    
    def is_valid_turn(self, x, y):
        return self.KB.in_board(x, y) and not self.KB.in_path(x, y)
    
    def update_perception(self, x, y, for_attack = False):
        if for_attack == True:
            self.KB.kill_Wumpus(x, y)
            if self.room.is_Empty(x, y):
                self.KB.add_empty(x, y)
        else:
            if self.room.is_Treasure(x, y):
                self.score += 1000
                self.room.collect_treasure(x, y)
                print("collect gold")
            if self.room.is_Empty(x, y):
                self.KB.add_empty(x, y)
            if self.room.is_Breeze(x, y):
                self.KB.add_Pit(x, y)
            if self.room.is_Stench(x, y):
                self.KB.add_Wumpus(x, y)
        
    def move_forward(self, x, y):
        self.Agent.update_position(x, y)
        self.KB.add_path((x, y))
        self.KB.add(x, y, "Empty")
        self.score -= 10
        self.room.update_agent_position(x, y)
        print("forward")
    
    def turn(self):
        self.Agent.turn_right()
        (x, y) = self.Agent.move_forward()
        if (self.is_valid_move(x, y)):
            print("right")
        else:
            self.Agent.turn_left()
            self.Agent.turn_left()
            print("left")

        self.room.update_agent_face(self.Agent.get_face())

    def turn_without_condition(self):
        self.Agent.turn_right()
        (x, y) = self.Agent.move_forward()
        if (self.KB.in_board(x, y)):
            print("right")
        else:
            self.Agent.turn_left()
            self.Agent.turn_left()
            print("left")

    def end_game(self):
        (x, y) = self.Agent.get_position()
        if self.room.is_Wumpus(x, y) or self.room.is_Pit(x, y):
            self.score -= 10000
            return True
        elif self.Agent.get_position == (0, -1):
            self.score += 10
            return True
        else:
            return False


    def get_solution(self):
        while not self.end_game():
            (x, y) = self.Agent.get_position()
            self.KB.add_path((x, y))
            self.Agent.add_queue((x, y), (x, y))
            while len(self.Agent.get_queue()) != 0:
                (x, y) = self.Agent.get_position()

                self.update_perception(x, y)

                if self.KB.can_t_go_further(x, y):
                    if self.KB.can_find_a_way(x, y):
                        (i, j) = self.Agent.move_forward()
                        if self.KB.maybe_a_Wumpus(i, j):
                            self.score -= 100
                            atack_successfully = self.room.Wumpus_take_an_attack(i, j)
                            if atack_successfully:
                                print("Shoot sucessfully")
                                self.update_perception(x, y, True)
                                self.move_forward(i, j)
                            else:
                                print("Miss!")
                        else:
                            self.turn()
                    else:
                        parent = self.Agent.back_to_parent()
                        if parent != (-1, -1):
                            self.KB.add_path(parent)
                            self.score -= 10
                            (x, y) = self.Agent.get_position()
                            self.room.update_agent_position(x, y)
                            print("backward")
                else:
                    (x, y) = self.Agent.move_forward()
                    if self.is_valid_move(x, y):
                        self.move_forward(x, y)
                    else:
                        self.turn()
            if not self.end_game():
                (x, y) = self.Agent.get_position()
                self.KB.add_path((x, y))
                self.Agent.add_queue((x, y), (x, y))
                self.turn_without_condition()
                (x, y) = self.Agent.move_forward()
                self.move_forward(x, y)

        return (self.KB.get_path() , self.score + 10)