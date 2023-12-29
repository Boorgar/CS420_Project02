class room:
    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read the size of the map (assuming it's the first character)
                size = int(file.readline().strip())

                # Read each line and create a matrix to represent the world
                world_map = []
                for _ in range(size):
                    line = file.readline().strip()
                    room_contents = line.split('.')
                    world_map.append(room_contents)

            self.size = size
            world_map.reverse()
            self.map = world_map

        except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                return None
        except Exception as e:
                print(f"Error reading file: {e}")
        return None
    
    def print_map(self):
         print(self.map)

    def is_Pit(self, x, y):
        return "P" in self.map[y][x]

    def is_Wumpus(self, x, y):
        return "W" in self.map[y][x]
    
    def is_Breeze(self, x, y):
        return "B" in self.map[y][x] 
    
    def is_Stench(self, x, y):
        return "S" in self.map[y][x]
    
    def is_Treasure(self, x, y):
         return "G" in self.map[y][x]
    
    def get_size(self):
        return self.size
    
    def get_map(self):
         return self.map
    
    def Wumpus_take_an_attack(self, x, y):
         if self.map[y][x] == "W":
              self.update_map_Wumpus_die(x, y)
              return True
         else:
              return False
         
    def update_map_Wumpus_die(self, x, y):
         self.map[y][x] = "_"
         candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
         for i, j in candidate:
            if self.in_board(i, j):
                if len(self.map[j][i]) == 1: 
                    self.map[j][i] = "_"
                else:
                    index_to_remove = self.map[j][i].find("S")
                    self.map[j][i] = self.map[j][i][:index_to_remove] + self.map[j][i][index_to_remove + 1:]

    def in_board(self, x, y):
        return x >= 0 and y >= 0 and x < self.size and y < self.size
    
    def collect_treasure(self, x, y):
         index_to_remove = self.map[y][x].find("G")
         self.map[y][x] = self.map[y][x][:index_to_remove] + self.map[y][x][index_to_remove + 1:]