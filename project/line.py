from utils.brick import BP, Motor, TouchSensor, EV3ColorSensor, wait_ready_sensors, reset_brick 
import time
import math

MOTORL = Motor("A") 
MOTORR = Motor("D")
MOTORPLAT = Motor("C")
MOTORKICK = Motor("B")
COLOR_SENSOR = EV3ColorSensor(1)
SIDE_COLOR_SENSOR = EV3ColorSensor(4)

POWER_LIMIT = 40
SPEED_LIMIT = 360

RW=0.028
RB=0.043
ORIENTTODEG = RB/RW
# set motor limits
print("sensors initializing")
wait_ready_sensors()

def check_color(rgb):
    means = [[0.987566201, 0.133367577, 0.080584644], [0.96937965, 0.2273774, 0.08586806], 
             [0.82395664, 0.55897973, 0.09190268], [0.407351948, 0.884058889, 0.227519999],
             [0.454594521, 0.480832567, 0.748704212], [0.967152296, 0.142217565, 0.209920143]]
    std_dev = [[0.00334054, 0.013688487, 0.015294446], [0.01000573, 0.02504622, 0.02241218],
               [0.00642989, 0.00992374, 0.00716117], [0.016844783, 0.010902598, 0.01834428], 
               [0.025688715, 0.022795108, 0.020173633], [0.003742952, 0.014803877,	0.0095453699]]
    
    color_names = ["RED", "ORANGE","YELLOW","GREEN","BLUE","PURPLE"]

    for i in range(len(means)):
        mean = means[i]
        stdev = std_dev[i]
        
        mR, mG, mB = mean
        sR, sG, sB = stdev
        denominator = math.sqrt(rgb[0]**2 + rgb[1]**2 + rgb[2]**2)
        if denominator == 0:
            return None
        r = rgb[0]/denominator
        g = rgb[1]/denominator
        b = rgb[2]/denominator

        diffR=(mR-r)/sR + 0.05  
        diffG=(mG-g)/sG + 0.05
        diffB=(mB-b)/sB + 0.05
        std_dist=math.sqrt(diffR**2 + diffG**2 + diffB**2)
        if i == 0:
            print(std_dist)
        if std_dist < 4:
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

def test_rotate():
    MOTORPLAT.set_position(360)
    MOTORPLAT.reset_encoder()

def rotate_platform(color):
    if color=="RED":
        MOTORPLAT.set_position(0)
    elif color=="ORANGE":
        MOTORPLAT.set_position(60)
    elif color=="YELLOW":
        MOTORPLAT.set_position(120)
    elif color=="GREEN":
        MOTORPLAT.set_position(180)
    elif color=="BLUE":
        MOTORPLAT.set_position(240)
    elif color=="PURPLE":
        MOTORPLAT.set_position(300)
    MOTORPLAT.reset_encoder()

def kick_block():
    MOTORKICK.set_position(135)
    MOTORKICK.reset_encoder()
    
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
            MOTORL.set_power(30)
            MOTORR.set_power(-30)
        elif color == "BLUE":
            print("blue")
            MOTORL.set_power(-30)
            MOTORR.set_power(30)
#         elif color == "GREEN":
#             print("green")
#             MOTORL.set_power(0)
#             MOTORR.set_power(0)
#             # find the zone
#             print("looking for zone")
#             zone_color = find_zone()
#             print("found " + str(zone_color) + " zone")
#             test_rotate()
#             #rotate_platform(color)
#             kick_block()
#             time.sleep(3)
#             MOTORL.set_position(90)
#             MOTORR.set_position(90)
#             continue

        else:
            MOTORL.set_power(20)
            MOTORR.set_power(20)
        
        time.sleep(0.1)
        # do smth with the rgb values

        
except KeyboardInterrupt:
    print("Ending by keyboard interrupt")
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()