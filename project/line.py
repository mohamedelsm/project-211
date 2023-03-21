from utils.brick import BP, Motor, TouchSensor, EV3ColorSensor, wait_ready_sensors, reset_brick 
import numpy as np
import time

MOTORL = Motor("A") 
MOTORR = Motor("D")
COLOR_SENSOR = EV3ColorSensor(4)

POWER_LIMIT = 40
SPEED_LIMIT = 360

RW=0.028
RB=0.043
ORIENTTODEG = RB/RW
# set motor limits
print("sensors initializing")
wait_ready_sensors()


def closest(color):
    colors = np.array([[175, 20, 12],[190, 36, 18],[200, 128, 22],[30, 68, 20],[22, 22, 33],[120,14,28]])
    colors_name = ["RED", "ORANGE","YELLOW","GREEN","BLUE","PURPLE"]
    color = np.array(color)

    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors_name[index_of_smallest[0][0]]
    return smallest_distance 


# main entry point
try:
    # motor initialization
    print("initialzing motors\n")
    MOTORL.set_limits(POWER_LIMIT, SPEED_LIMIT)
    MOTORR.set_limits(POWER_LIMIT, SPEED_LIMIT)
    MOTORL.set_power(30)
    MOTORR.set_power(30)

    while True:
        rgb = COLOR_SENSOR.get_rgb()
        print(rgb)
        color = closest(rgb)

        if color == "RED":
            print("red")
            MOTORL.set_power(-15)
            MOTORR.set_power(70)
        elif color == "BLUE":
            print("blue")
            MOTORL.set_power(70)
            MOTORR.set_power(-15)
        elif color == "GREEN":
            print("green")
            MOTORL.set_power(0)
            MOTORR.set_power(0)
        else:
            MOTORL.set_power(20)
            MOTORR.set_power(20)
        
        time.sleep(0.1)

        # do smth with the rgb values

        
            
except KeyboardInterrupt:
    print("Ending by keyboard interrupt")
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()