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

def check_color():
    # change rgb sensor
    rgb = COLOR_SENSOR.get_rgb()
    R=rgb[0]
    G=rgb[1]
    B=rgb[2]

    if R in range(110,190) and G in range(10,28) and B in range(10,16):
        return "RED"
    elif R in range(15,30) and G in range(15,30) and B in range(25,40):
        return "BLUE"
    elif R in range(15,45) and G in range(40,75) and B in range(5,25):
        return "GREEN"
    elif R in range(175, 205) and G in range(28, 45) and B in range(10,25):
        return "ORANGE"
    elif R in range(180, 220) and G in range(120, 135) and B in range(17,27):
        return "YELLOW"
    elif R in range(100, 140) and G in range(8, 20) and B in range(20,35):
        return "PURPLE"
    else:
        return None
    
def find_zone():
    while True:
        # turn for a bit
        MOTORL.set_power(55)
        MOTORR.set_power(-50)
        time.sleep(2)

        # go forward and look for color
        MOTORL.set_power(20)
        MOTORL.set_power(20)
        t_end = time.time() + 60 * 2
        while time.time() < t_end:
            # check for the color
            color = check_color()
            if color != None:
                MOTORL.set_power(0)
                MOTORL.set_power(0)
                return color
            
        # go back to original position
        MOTORL.set_power(-20)
        MOTORL.set_power(-20)
        time.sleep(2)

def reset_motor(): 
    MOTORL.set_dps(0)
    MOTORL.set_dps(0)
    MOTORL.set_power(0)
    MOTORR.set_power(0)  
    

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
            MOTORL.set_power(-50)
            MOTORR.set_power(50)
        elif color == "BLUE":
            print("blue")
            MOTORL.set_power(50)
            MOTORR.set_power(-50)
        elif color == "GREEN":
            print("green")
            MOTORL.set_power(0)
            MOTORR.set_power(0)
            # find the zone
            print("looking for zone")
            zone_color = find_zone()
            print("found " + str(zone_color) + " zone")
        else:
            MOTORL.set_power(20)
            MOTORR.set_power(20)
        
        time.sleep(0.1)
        # do smth with the rgb values

        
except KeyboardInterrupt:
    print("Ending by keyboard interrupt")
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()