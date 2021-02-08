from sense_hat import SenseHat

import time

sense = SenseHat()

class DirectionInput:
    def __init__(self):
        pass

    def direction(self):
	acceleration = sense.get_accelerometer_raw()
	x = acceleration['x']
	y = acceleration['y']
	z = acceleration['z']

	x=round(x, 1)
	y=round(y, 1)
	z=round(z, 1)

        if x >= 0.5:
            direction = 'e'
        elif x <= -0.5:
            direction = 'w'
        elif y >= 0.5:
            direction = 'n'
        elif y <= -0.5:
            direction = 's'
        else:
            direction = '?'

        return direction

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
        #print(self.path)

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
        #print(out_of_bounds)
        return out_of_bounds

class Game:
    def __init__(self):
        self.direction_input = DirectionInput()
        self.current_direction = 'w'

    def set_current_direction(self):
        compass = ['n', 'e', 's', 'w']
        sensed_direction = self.direction_input.direction()
        if sensed_direction == '?':
            return
        compass_difference = abs(compass.index(self.current_direction) - compass.index(sensed_direction))
        if compass_difference == 1 or compass_difference == 3:
            self.current_direction = sensed_direction

    def initalize(self):
        sense.clear((0, 0, 0))
        self.snake_last_moved = self.millis()
        self.brian = Snake([(2,4),(3,4),(4,4)], self.current_direction)
        self.brian.draw()

    def millis(self):
        return int(time.time()*1000)

    def move(self):
        #print self.millis() - self.snake_last_moved
        if self.millis() - self.snake_last_moved > 500:
            if self.brian.is_out_of_bounds() == False:
                #print("moving snake")
                self.brian.move(self.current_direction)
                self.snake_last_moved = self.millis()

    def run(self):
        while True:
            self.set_current_direction()
            self.move()
            if self.brian.is_out_of_bounds() == True:
                break


game = Game()
game.initalize()
game.run()

