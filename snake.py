#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
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
    width = 8
    height = 8

    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear((0, 0, 0))

    def set_pixel(self, x, y, color = (255, 255, 255)):
        self.sense.set_pixel(x, y, color)

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

        threshold = 0.2
        if x >= threshold:
            direction = 'e'
        elif x <= -threshold:
            direction = 'w'
        elif y >= threshold:
            direction = 'n'
        elif y <= -threshold:
            direction = 's'
        else:
            direction = '?'

        return direction

    def show_letter(self, letter):
        self.sense.show_letter(letter, (0, 0, 255))
    
class Egg:
    red = (255, 0, 0)

    def __init__(self, environment, illegal_points):
        self.environment = environment
        self.illegal_points = illegal_points
        self.__place()
        
    def __place(self):
        while True:
            self.x = random.randint(0, self.environment.width - 1)
            self.y = random.randint(0, self.environment.height - 1)
            if ((self.x, self.y) in self.illegal_points) == False:
                break

        self.environment.set_pixel(self.x, self.y, self.red)

    def location(self):
        return (self.x, self.y)

class Snake:

    def __init__(self, path, direction, environment):
        self.path = path
        self.direction = direction
        self.environment = environment

    def head(self):
        return self.path[0]

    def draw(self):
        for pixel in self.path:
            self.environment.set_pixel(pixel[0], pixel[1])

    def move(self, direction, grow):
        if grow == False:
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
        if head[0] > self.environment.width - 1 or head[0] < 0 or head[1] > self.environment.height - 1 or head[1] < 0:
            out_of_bounds = True

        return out_of_bounds

    def is_collided(self):
        head = self.path[0]
        collided = False
        for point in self.path[1:]:
            if point == head:
                collided = True
                break
        return collided

    def is_snake_dead(self):
        return self.is_out_of_bounds() or self.is_collided()


class Proximity:

    def __init__(self, snake, egg):
        self.snake = snake
        self.egg = egg
    
    def is_eaten(self):
        return self.snake.head() == self.egg.location()


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
        self.brian = Snake([(2, 4), (3, 4), (4, 4)],
                           self.current_direction, self.environment)
        self.brian.draw()
        self.egg = Egg(self.environment, self.brian.path)
        self.last_move_ate_egg = False
        self.score = 0

    def millis(self):
        return int(time.time() * 1000)

    def print_score(self):
        self.environment.show_letter(str(self.score))

    def tick(self):
        if self.brian.is_out_of_bounds() == False:
            self.brian.move(self.current_direction, self.last_move_ate_egg)
            self.last_move_ate_egg = Proximity(self.brian, self.egg).is_eaten() 
            if self.last_move_ate_egg == True:
                self.egg = Egg(self.environment, self.brian.path)
                self.score += 1

    def run(self):
        last_tick = self.millis()

        while True:
            if self.millis() - last_tick > 500:
                self.tick()
                last_tick = self.millis()
            self.set_current_direction()
            if self.brian.is_snake_dead() == True:
                break
        self.print_score()
        self.environment.end()

game = Game()
game.initalize()
game.run()

