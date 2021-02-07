from sense_hat import SenseHat
sense = SenseHat()
sense.clear()
import time
o = sense.get_orientation()


while True:
    p = o
    o = sense.get_orientation()
    pitch_d = o["pitch"] - p["pitch"]
    roll_d = o["roll"] - p["roll"]
    yaw_d = o["yaw"] - p["yaw"]
    print("pitch {0} roll {1} yaw {2}".format(round(pitch_d,0), round(roll_d,0), round(yaw_d,0)))

    #if pitch > 300:
    #    print "east"
   # 
  #  if pitch < 100:
  #      print "west"
   
  #  if roll > 300:
  #      print "south"
   
  #  if roll < 100:
  #      print "north"




    time.sleep(1)
