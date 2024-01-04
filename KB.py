
class Pit:
    def __init__(self):
        self.list = []
    
    def add(self, x, y):
        self.list.append((x, y))

    def get_list(self):
        return self.list
    
    def clear(self, x, y):
        for index, element in enumerate(self.list):
            if element == (x, y):
                self.list.pop(index)
                break
            

class Wumpus:
    def __init__(self):
        self.list = []
    
    def add(self, x, y):
        self.list.append((x, y))

    def get_list(self):
        return self.list
    
    def clear(self, x, y):
        for index, element in enumerate(self.list):
            if element == (x, y):
                break

        self.list.pop(index)
    
    def in_Wumpus_list(self, x, y):
        return (x, y) in self.list


class knowledge_base:
    def __init__(self, size):
        self.Pit = Pit()
        self.Wumpus = Wumpus()
        self.action = []
        self.size = size
        self.path = []
        self.stuck_list = []
        self.action_history = []
    
    def add_action(self, clause):
        self.action.append(clause)

    def add_action_history(self, clause):
        self.action_history.append(clause)

    def get_action_history(self):
        return self.action_history

    def get_previous_action(self):
        return self.action[-1]
    
    def is_empty_action(self):
        return len(self.action) == 0
    
    def back_to_previous_action(self):
        self.action.pop()

    def in_board(self, x, y):
        if self.totally_stuck() and (x, y) == (0, -1):
            return True
        return x >= 0 and y >= 0 and x < self.size and y < self.size

    def add_Pit(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
            if not (i, j) in self.path and self.in_board(i, j):
                self.Pit.add(i, j)
    
    def add_Wumpus(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
            if not (i, j) in self.path and self.in_board(i, j) and not (i, j) in self.Wumpus.get_list():
                self.Wumpus.add(i, j)
    
    def add_empty(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
            if not (i, j) in self.path and self.in_board(i, j):
                if (i, j) in self.Pit.get_list():
                    self.Pit.clear(i, j)
                if (i, j) in self.Wumpus.get_list():
                    self.Wumpus.clear(i, j)
    
    def can_t_go_further(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
            if not (i, j) in self.path and self.in_board(i, j) and not self.danger(i, j):
                return False
        return True
    
    def can_find_a_way(self, x, y):
        list = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in list:
            if self.in_board(i, j) and self.Wumpus.in_Wumpus_list(i, j):
                return True
        return False
    
    def add_stuck(self, x, y):
        for index, element in enumerate(self.path):
            if element == (x, y):
                self.stuck_list[index] = True

    def totally_stuck(self):
        for element in self.stuck_list:
            if element == False:
                return False
        return True
    
    def danger(self, x, y):
        return (x, y) in self.Pit.get_list() or self.Wumpus.in_Wumpus_list(x, y)
    
    def add_path(self, x):
        self.path.append(x)
        self.stuck_list.append(False)
    
    def in_path(self, x, y):
        return (x, y) in self.path

    def maybe_a_Wumpus(self, x, y):
        return self.Wumpus.in_Wumpus_list(x, y)
    
    def kill_Wumpus(self, x, y):
        list = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in list:
            if (i, j) in self.Wumpus.get_list():
                self.Wumpus.clear(i, j)

    def get_path(self):
        return self.path
