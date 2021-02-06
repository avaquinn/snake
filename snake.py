from sense_hat import SenseHat

sense = SenseHat()

class Snake:
    def __init__(self, path, direction):
        self.path = path
        self.direction = direction

    def draw(self):
       white = (255, 255, 255)
       for pixel in self.path:
           sense.set_pixel(pixel[0], pixel[1], white)


sense.clear((0, 0, 0))
brian = Snake([(5,4),(6,4),(7,4)],'w')
brian.draw()







