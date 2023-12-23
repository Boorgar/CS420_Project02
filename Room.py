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
            self.map = world_map

        except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                return None
        except Exception as e:
                print(f"Error reading file: {e}")
        return None
    
    def print_map(self):
         print(self.map)