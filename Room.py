class room:
    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as file:
                size = int(file.readline().strip())

                world_map = []
                for _ in range(size):
                    line = file.readline().strip()
                    room_contents = line.split('.')
                    world_map.append(room_contents)


            self.size = size
            world_map.reverse()
            self.map = world_map
            self.x = 0
            self.y = 0
            self.face = "right"
            self.generate_enviroment()
            self.print_world_map_to_file(self.size, self.map, "Output.txt")


        except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                return None
        except Exception as e:
                print(f"Error reading file: {e}")
        return None
    
    def print_world_map_to_file(self, size, world_map, output_file_path):
        try:
            map = world_map
            #map.reverse()
            with open(output_file_path, 'w') as output_file:
                output_file.write(f"Size: {size}\n")
                output_file.write("World Map:\n")
                for row in map:
                    output_file.write(' '.join(row) + '\n')
    
            print(f"World map printed to {output_file_path}")
        except Exception as e:
            print(f"Error writing to file: {e}")

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
    
    def is_Empty(self, x, y):
        return self.map[y][x] == "A"
    
    def get_size(self):
        return self.size
    
    def get_map(self):
         return self.map
    
    def Wumpus_take_an_attack(self, x, y):
         if "W" in self.map[y][x]:
              self.update_map_Wumpus_die(x, y)
              return True
         else:
              return False
         
    def adjent_wumpus_or_Pitt(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
           if self.in_board(i, j):
                if self.map[j][i] == "W" or self.map[j][i] == "P":
                     return True
        return False
    
    def adjent_wumpus(self, x, y):
        candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for i, j in candidate:
           if self.in_board(i, j):
                if self.map[j][i] == "W":
                     return True
        return False

    def update_map_Wumpus_die(self, x, y):
         self.map[y][x] = ""
         candidate = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
         for i, j in candidate:
            if self.in_board(i, j) and not self.adjent_wumpus(i, j):
                if self.map[j][i] == "S": 
                    self.map[j][i] = "-"
                else:
                    index_to_remove = self.map[j][i].find("S")
                    self.map[j][i] = self.map[j][i][:index_to_remove] + self.map[j][i][index_to_remove + 1:]
            if self.in_board(i, j) and self.map[j][i] == "P":
                if "P" not in self.map[y][x]:
                    self.map[y][x] += "B"
            elif self.in_board(i, j) and self.map[j][i] == "W":
                if "P" not in self.map[j][i]:
                    self.map[y][x] += "S"
         if len(self.map[y][x]) == 0:
            self.map[y][x] == "-"

    def in_board(self, x, y):
        return x >= 0 and y >= 0 and x < self.size and y < self.size
    
    def collect_treasure(self, x, y):
        index_to_remove = self.map[y][x].find("G")
        self.map[y][x] = self.map[y][x][:index_to_remove] + self.map[y][x][index_to_remove + 1:]
        
    def generate_enviroment(self):
        for i in range(self.size):
             for j in range(self.size):
                  list = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                  if self.map[i][j] == "P":
                       for k, l in list:
                            if self.in_board(k, l):
                                 if "B" not in self.map[k][l] and "P" not in self.map[k][l] and "W" not in self.map[k][l]:
                                    if self.map[k][l] == "-":
                                         self.map[k][l] = "B"
                                    else:
                                         self.map[k][l] += "B"
                  if self.map[i][j] == "W":
                       for k, l in list:
                            if self.in_board(k, l):
                                 if "S" not in self.map[k][l] and "P" not in self.map[k][l] and "W" not in self.map[k][l]:
                                    if self.map[k][l] == "-":
                                         self.map[k][l] = "S"
                                    else:
                                         self.map[k][l] += "S"
                  if "A" in self.map[i][j] :
                        self.x = j
                        self.y = i
    
    def get_agent_position(self):
         return self.x, self.y
    
    def update_agent_position(self, x, y):
         if self.map[self.y][self.x] == "A":
            self.map[self.y][self.x] += "-"
         index = self.map[self.y][self.x].find("A")
         self.map[self.y][self.x] = self.map[self.y][self.x][:index] + self.map[self.y][self.x][index + 1:]
         self.x = x
         self.y = y
         if self.map[y][x] == "-":
            self.map[y][x] = "A"
         else:
            self.map[y][x] += "A"

    def update_agent_face(self, face):
         self.face = face
                            