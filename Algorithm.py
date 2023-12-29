import Agent
import KB

class Solution:
    def __init__(self, room):
        self.Agent = Agent.Agent()
        self.room = room
        self.KB = KB.knowledge_base(self.room.get_size())
        self.score = 0
    
    def is_valid_move(self, x, y):
        return self.KB.in_board(x, y) and not self.KB.danger(x, y) and not self.KB.in_path(x, y)
    
    def is_valid_turn(self, x, y):
        return self.KB.in_board(x, y) and not self.KB.in_path(x, y)
    
    def update_perception(self, x, y, for_attack = False):
        if for_attack == True:
            self.KB.kill_Wumpus(x, y)
        else:
            if self.room.is_Breeze(x, y):
                self.KB.add_Pit(x, y)
            if self.room.is_Stench(x, y):
                self.KB.add_Wumpus(x, y)
        

    def get_solution(self):
        self.KB.add_path((0, 0))
        self.Agent.add_queue((0, 0), (0, 0))
        while len(self.Agent.get_queue()) != 0:
            (x, y) = self.Agent.get_position()

            if self.room.is_Treasure(x, y):
                self.score += 1000
                self.room.collect_treasure(x, y)
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
                            self.Agent.update_position(i, j)
                            self.KB.add_path((i, j))
                            self.KB.add(i, j, "Empty")
                            self.score -= 10
                            print("forward")
                        else:
                            print("Miss!")
                    else:
                        self.Agent.turn_right()
                        (i, j) = self.Agent.move_forward()
                        if (self.is_valid_turn(i, j)):
                            print("right")
                        else:
                            self.Agent.turn_left()
                            self.Agent.turn_left()
                            print("left")
                else:
                    parent = self.Agent.back_to_parent()
                    self.KB.add_path(parent)
                    self.score -= 10
                    print("backward")
            else:
                (x, y) = self.Agent.move_forward()
                if self.is_valid_move(x, y):
                    self.Agent.update_position(x, y)
                    self.KB.add_path((x, y))
                    self.KB.add(x, y, "Empty")
                    self.score -= 10
                    print("forward")
                else:
                    self.Agent.turn_right()
                    (x, y) = self.Agent.move_forward()
                    if (self.is_valid_move(x, y)):
                        print("right")
                    else:
                        self.Agent.turn_left()
                        self.Agent.turn_left()
        return (self.KB.get_path() , self.score + 10)