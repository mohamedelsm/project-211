from utils.brick import BP, Motor, TouchSensor, EV3ColorSensor, wait_ready_sensors, reset_brick 
import time
import math

MOTORL = Motor("D") 
MOTORR = Motor("A")
MOTORPLAT = Motor("C")
MOTORKICK = Motor("B")
COLOR_SENSOR = EV3ColorSensor(4)
SIDE_COLOR_SENSOR = EV3ColorSensor(1)

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
        if rgb == [None, None, None]:
            return None
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
        if std_dist < 4:
            return color_names[i]
            
    return None

def orient():
    if prev_color=='BLUE':
        MOTORR.set_power(-20)
        MOTORL.set_power(20)
        time.sleep(1.5)
        MOTORR.set_power(0)
        MOTORL.set_power(0)
    
    elif prev_color=='RED':
        MOTORL.set_power(-12)
        MOTORR.set_power(12)
        time.sleep(1.5)
        MOTORR.set_power(0)
        MOTORL.set_power(0)
        
    MOTORR.set_power(20)
    MOTORL.set_power(20)
    time.sleep(1)
    MOTORR.set_power(0)
    MOTORL.set_power(0)
    time.sleep(2)
        
    
def find_zone():
    print("finding zone")
    # turn for a bit
#     MOTORL.set_power(30)
#     MOTORR.set_power(-30)
#     time.sleep(0.2)
    rgb = SIDE_COLOR_SENSOR.get_rgb()
    color = check_color(rgb)
        # go forward and look for color
#         print("going forward")
#         MOTORL.set_power(20)
#         MOTORR.set_power(20)
#       time.sleep(1)
        #print("going forward done")
#         t_end = time.time() + 2
#         while time.time() < t_end:
#             print(time.time())
            # check for the color
    
    if color == None and prev_color == "BLUE": #swivel around backwards to find zone
        while color == None:
            print("shifting cuz prev blue")
            MOTORL.set_power(20)
            MOTORR.set_power(-20)
            time.sleep(0.25)
            rgb = SIDE_COLOR_SENSOR.get_rgb()
            color = check_color(rgb)
    elif color == None and prev_color == "RED": #swivel around backwards to find zone
        while color == None:
            print("shifting cuz prev red")
            MOTORL.set_power(-20)
            MOTORR.set_power(20)
            time.sleep(0.25)
            rgb = SIDE_COLOR_SENSOR.get_rgb()
            color = check_color(rgb)

    print("found deliv zone color:"+ color)
#           MOTORL.set_power(0)
#           MOTORR.set_power(0)
    return color
        
#         cond=True
#         while cond==True: #starting looking for deliv color again
#             rgb = COLOR_SENSOR.get_rgb()
#             while check_color(rgb) != None: #move forward until you detect white
#                 MOTORR.set_power(10)
#                 MOTORL.set_power(10)
#                 cond=False
#         MOTORR.set_power(0)
#         MOTORL.set_power(0) #stop right when u exit deliv zone (drop block behind)
#         print("out of deliv zone!")
        
#         print("loop done")
#         # go back to original position
#         MOTORL.set_power(-20)
#         MOTORR.set_power(-20)
#         time.sleep(2)
#         # turn for a bit
#         MOTORL.set_power(30)
#         MOTORR.set_power(-30)
#         time.sleep(0.2)

def rotate_platform(color):
    if color=="RED":
        angle=0
    elif color=="ORANGE":
        angle=60
    elif color=="YELLOW":
        angle=120
    elif color=="GREEN":
        angle=180
    elif color=="BLUE":
        angle=240
    elif color=="PURPLE":
        angle=300
    MOTORPLAT.reset_encoder()
    return angle

def test_rotate():
    MOTORPLAT.set_limits(30)
    MOTORPLAT.set_position(360)
    time.sleep(1.15)
    kick_block()
    time.sleep(1.5)
    MOTORPLAT.set_position(0)

def kick_block():
    reset_motor()
    MOTORKICK.set_limits(20)
    MOTORKICK.set_position(135)
    time.sleep(1)
    MOTORKICK.set_position(0)
    
def reset_motor(): 
    MOTORL.set_dps(0)
    MOTORL.set_dps(0)
    MOTORL.set_power(0)
    MOTORR.set_power(0)
    
def move_out_of_zone():
    rgb = SIDE_COLOR_SENSOR.get_rgb()
    color = check_color(rgb)
    while color != None:
        MOTORR.set_power(10)
        MOTORL.set_power(10)
        time.sleep(0.4)
        rgb = SIDE_COLOR_SENSOR.get_rgb()
        color = check_color(rgb)
    MOTORR.set_power(0)
    MOTORL.set_power(0)
    print("out of zone!")
    MOTORPLAT.set_limits(20)
    test_rotate()
    time.sleep(2)
    
# main entry point
try:
    blocks_delivered=0
    while blocks_delivered<6:
        # motor initialization
        print("initialzing motors\n")
        MOTORL.set_limits(POWER_LIMIT, SPEED_LIMIT)
        MOTORR.set_limits(POWER_LIMIT, SPEED_LIMIT)
        MOTORL.set_power(-20)
        MOTORR.set_power(20)
        MOTORKICK.reset_encoder()
        while True:
            rgb = COLOR_SENSOR.get_rgb()
            print(rgb)
            color = check_color(rgb)
            print(color)
            if color == "RED":
                print("red")
                prev_color=color
                MOTORL.set_power(-30)
                MOTORR.set_power(30)
            elif color == "BLUE":
                prev_color=color
                print("blue")
                MOTORL.set_power(30)
                MOTORR.set_power(-30)
            elif color == "GREEN":
                print("green")
                reset_motor()
                time.sleep(1) #stop for a sec to emphasize sensing green
                # find the zone
                print("looking for zone")
                orient() #function by matt
                zone_color = find_zone()
                move_out_of_zone()
                blocks_delivered+=1
                time.sleep(2)

                # test_rotate()
                # #rotate_platform(color)
                # kick_block()
                # time.sleep(3)
                # MOTORL.set_position(90)
                # MOTORR.set_position(90)
                # continue

            else:
                MOTORL.set_power(10)
                MOTORR.set_power(35)
            
    #         if color!= None and color!="GREEN":
    #             prev_color=color
    #             print("HELLO"+ str(prev_color))
            
            print("Blocks left: "+str((6-blocks_delivered)))
            time.sleep(0.1)
            # do smth with the rgb values

        
except KeyboardInterrupt:
    print("Ending by keyboard interrupt")
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()