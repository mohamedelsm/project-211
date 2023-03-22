from utils.brick import BP, Motor, TouchSensor, EV3ColorSensor, wait_ready_sensors, reset_brick 
import time
import math

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

def check_color(rgb):
    means = [[0.82230793, 0.11083375, 0.06685832], [0.75654495, 0.17690667, 0.06654838], 
             [0.5586913, 0.37901136, 0.06229734], [0.26811848, 0.58220407, 0.14967744],
             [0.26986127, 0.28546987, 0.44466886], [0.73325641, 0.10767692, 0.15906667]]
    std_dev = [[0.0186642, 0.00907358, 0.01105631], [0.02676107, 0.01332406, 0.01422075],
               [0.00557763, 0.00658229, 0.0046249], [0.00875172, 0.01423021, 0.01032464], 
               [0.01389173, 0.01254777, 0.01502582], [0.01269495, 0.00986052, 0.00567139]]
    
    color_names = ["RED", "ORANGE","YELLOW","GREEN","BLUE","PURPLE"]

    for i in range(len(means)):
        mean = means[i]
        stdev = std_dev[i]
        
        mR, mG, mB = mean
        sR, sG, sB = stdev
        r, g, b =rgb

        diffR=(mR-r)/sR   
        diffG=(mG-g)/sG
        diffB=(mB-b)/sB
        std_dist=math.sqrt(diffR**2 + diffG**2 + diffB**2)

        if std_dist < 2:
            return color_names[i]
            
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
        color = check_color(rgb)
        print(color)
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