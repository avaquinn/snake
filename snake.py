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
        else :
            raise Exception("Invalid direction")
        self.path.insert(0,new_head)
        sense.set_pixel(new_head[0], new_head[1], self.white)

    def remove_tail(self):
       tail = self.path[-1]
       sense.set_pixel(tail[0], tail[1], self.black)
       self.path = self.path[:-1]


sense.clear((0, 0, 0))
brian = Snake([(5,4),(6,4),(7,4)],'w')
brian.draw()

for i in range(3):
    time.sleep(0.5)
    brian.move('w')

for i in range(2):
    time.sleep(0.5)
    brian.move('n')

