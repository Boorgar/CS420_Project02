
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
        self.count_list = []
    
    def add(self, x, y):
        if (x, y) in self.list:
            index = self.list.index((x, y))
            self.count_list[index] += 1
        else:
            self.list.append((x, y))
            self.count_list.append(1)

    def get_list(self):
        return self.list
    
    def clear(self, x, y):
        for index, element in enumerate(self.list):
            if element == (x, y):
                break

        self.count_list[index] -= 1
        if self.count_list[index] == 0:
            self.list.pop(index)
            self.count_list.pop(index)
    
    def in_Wumpus_list(self, x, y):
        return (x, y) in self.list


class knowledge_base:
    def __init__(self, size):
        self.Pit = Pit()
        self.Wumpus = Wumpus()
        self.KB = []
        self.size = size
        self.path = []
    
    def add(self, x, y, clause):
        self.KB.append((x, y , clause))
    
    def in_board(self, x, y):
        return x >= 0 and y >= 0 and x < self.size and y < self.size

    def add_Pit(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
            if not (i, j) in self.path and self.in_board(i, j):
                self.Pit.add(i, j)
    
    def add_Wumpus(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
            if not (i, j) in self.path and self.in_board(i, j):
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
    
    def danger(self, x, y):
        return (x, y) in self.Pit.get_list() or self.Wumpus.in_Wumpus_list(x, y)
    
    def add_path(self, x):
        self.path.append(x)
    
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
