import time
from sense_hat import SenseHat

sense = SenseHat()

direction = "north"
while True:
        p_direction = direction
	acceleration = sense.get_accelerometer_raw()
	x = acceleration['x']
	y = acceleration['y']
	z = acceleration['z']

	x=round(x, 1)
	y=round(y, 1)
	z=round(z, 1)

        #print("x={0}, y={1}, z={2}".format(x, y, z))
        time.sleep(0.05)
        
        if x >= 0.5:
            direction = "west"
        if x <= -0.5:
            direction = "east"
        if y >= 0.5:
            direction = "north"
        if y <= -0.5:
            direction = "south"

        if p_direction != direction:
            print(direction)

