from sense_hat import SenseHat

import time

sense = SenseHat()

class Snake:
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self, path, direction):
        self.path = path
        self.direction = direction

    def draw(self):
       for pixel in self.path:
            sense.set_pixel(pixel[0], pixel[1], self.white)
   
    def move(self, direction):
        self.remove_tail()
        self.add_head(direction)
        print(self.path)

    def add_head(self, direction):
        old_head = self.path[0]
        if direction == 'w':
            new_head = (old_head[0] -1, old_head[1])
        elif direction == 'n':
            new_head = (old_head[0], old_head[1] +1)
        elif direction == 'e':
            new_head = (old_head[0] +1, old_head[1])
        elif direction == 's':
            new_head = (old_head[0], old_head[1] -1)
        else:
            raise Exception("Invalid direction")
        self.path.insert(0,new_head)
        if self.is_out_of_bounds() == False:
            sense.set_pixel(new_head[0], new_head[1], self.white)
            
    def remove_tail(self):
       tail = self.path[-1]
       sense.set_pixel(tail[0], tail[1], self.black)
       self.path = self.path[:-1]

    def is_out_of_bounds(self):
        out_of_bounds = False
        head = self.path[0]
        if head[0] > 7 or head[0] < 0 or head[1] > 7 or head[1] < 0:
            out_of_bounds = True
        print(out_of_bounds)
        return out_of_bounds

class Game:
    def __init__(self):
        pass

    def initalize(self):
        sense.clear((0, 0, 0))
        self.brian = Snake([(2,4),(3,4),(4,4)],'w')
        self.brian.draw()

    def run(self):
        while self.brian.is_out_of_bounds() == False:
            time.sleep(0.5)
            self.brian.move('n')


game = Game()
game.initalize()
game.run()

