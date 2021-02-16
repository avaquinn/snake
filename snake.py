#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from sense_hat import SenseHat 

class CursesEnvironment:

    import curses as curses

    def __init__(self):
        self.screen = self.curses.initscr()
        self.screen.nodelay(True)  # non-blocking keyboard input

    def set_pixel(self, x, y):
        self.screen.addstr(y, x, '@')
        self.screen.refresh()

    def delete_pixel(self, x, y):
        self.screen.addstr(y, x, ' ')
        self.screen.refresh()

    def end(self):
        self.curses.endwin()

    def direction_input(self):
        direction_map = {
            'w': 'n',
            'a': 'w',
            's': 's',
            'd': 'e',
            }

        keyboard_input = self.screen.getch()
        if keyboard_input in direction_map.keys():
            #print keyboard_input
            direction = direction_map[keyboard_input]
        else:
            direction = '?'

        return direction


class SenseHatEnvironment:
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear((0, 0, 0))

    def set_pixel(self, x, y):
        self.sense.set_pixel(x, y, self.white)

    def delete_pixel(self, x, y):
        self.sense.set_pixel(x, y, self.black)

    def end(self):
        pass

    def direction_input(self):
        acceleration = self.sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = round(x, 1)
        y = round(y, 1)
        z = round(z, 1)

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


    def __init__(self, path, direction, environment):
        self.path = path
        self.direction = direction
        self.environment = environment

    def draw(self):
        for pixel in self.path:
            self.environment.set_pixel(pixel[0], pixel[1])

    def move(self, direction):
        self.remove_tail()
        self.add_head(direction)

        # print(self.path)

    def add_head(self, direction):
        old_head = self.path[0]
        if direction == 'w':
            new_head = (old_head[0] - 1, old_head[1])
        elif direction == 'n':
            new_head = (old_head[0], old_head[1] + 1)
        elif direction == 'e':
            new_head = (old_head[0] + 1, old_head[1])
        elif direction == 's':
            new_head = (old_head[0], old_head[1] - 1)
        else:
            raise Exception('Invalid direction')
        self.path.insert(0, new_head)
        if self.is_out_of_bounds() == False:
            self.environment.set_pixel(new_head[0], new_head[1])

    def remove_tail(self):
        tail = self.path[-1]
        self.environment.delete_pixel(tail[0], tail[1])
        self.path = self.path[:-1]

    def is_out_of_bounds(self):
        out_of_bounds = False
        head = self.path[0]
        if head[0] > 7 or head[0] < 0 or head[1] > 7 or head[1] < 0:
            out_of_bounds = True

        # print(out_of_bounds)

        return out_of_bounds


class Game:

    def __init__(self):
        self.current_direction = 'w'
        #self.environment = CursesEnvironment()
        self.environment = SenseHatEnvironment()

    def set_current_direction(self):
        compass = ['n', 'e', 's', 'w']

        sensed_direction = self.environment.direction_input()

        if sensed_direction == '?':
            return
        compass_difference = abs(compass.index(self.current_direction)
                                 - compass.index(sensed_direction))
        if compass_difference == 1 or compass_difference == 3:
            self.current_direction = sensed_direction

    def initalize(self):
        self.snake_last_moved = self.millis()
        self.brian = Snake([(2, 4), (3, 4), (4, 4)],
                           self.current_direction, self.environment)
        self.brian.draw()

    def millis(self):
        return int(time.time() * 1000)

    def move(self):

        # print self.millis() - self.snake_last_moved

        if self.millis() - self.snake_last_moved > 500:
            if self.brian.is_out_of_bounds() == False:

                # print("moving snake")

                self.brian.move(self.current_direction)
                self.snake_last_moved = self.millis()

    def run(self):
        while True:
            self.set_current_direction()
            self.move()
            if self.brian.is_out_of_bounds() == True:
                break
        self.environment.end()


game = Game()
game.initalize()
game.run()
