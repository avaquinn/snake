from sense_hat import SenseHat
import time

sense = SenseHat()

sense.clear()
while True:
    for x in range(8):
        sense.set_pixel(x, 2, (0, 0, 255))
        time.sleep(0.1)
        sense.clear()

