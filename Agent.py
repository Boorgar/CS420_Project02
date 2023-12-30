class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.queue = []
        self.actions = []
        self.face = "right"

    def move_forward(self):
        x = self.x
        y = self.y
        match self.face:
            case "right":
                x += 1
            case "left":
                x -= 1
            case "up":
                y += 1
            case "down":
                y -= 1

        return x, y
        
    def move_backward(self):
        x = self.x
        y = self.y
        match self.face:
            case "right":
                x -= 1
            case "left":
                x += 1
            case "up":
                y -= 1
            case "down":
                y += 1
        
        return x, y

    def turn_left(self):
        match self.face:
            case "right":
                self.face = "up"
            case "left":
                self.face = "down"
            case "up":
                self.face = "left"
            case "down":
                self.face = "right"
    
    def turn_right(self):
            match self.face:
                case "right":
                    self.face = "down"
                case "left":
                    self.face = "up"
                case "up":
                    self.face = "right"
                case "down":
                    self.face = "left"
    
    def get_position(self):
        return (self.x, self.y)
    
    def update_position(self, x, y):
        self.add_queue((self.x, self.y), (x, y))
        self.x = x
        self.y = y

    def back_to_parent(self):
        if len(self.queue) > 1:
            last_element = self.queue[-1]
            self.x = last_element[0][0]
            self.y = last_element[0][1]
            self.queue.pop()
            return (self.x, self.y)
        else:
            self.queue.pop()
            return(-1, -1)

    def add_action(self, x):
        self.actions.append(x)

    def add_queue(self, child, parent):
        self.queue.append((child, parent))

    def get_queue(self):
        return self.queue
    
    def get_face(self):
        return self.face