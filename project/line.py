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

def side_check_color(rgb):
    means = [[0.98269282, 0.166543148, 0.079804332], [0.956722739, 0.279694185, 0.075963383], 
             [0.736488044, 0.672059319, 0.075039654], [0.313354802, 0.927045185, 0.202401399],
             [0.368746318, 0.608397841, 0.698980325], [0.963167792, 0.175536085, 0.201083857]]
    std_dev = [[0.004002433, 0.016609388, 0.01300176], [0.00668939, 0.023818665, 0.008397344],
               [0.00948927, 0.009867564, 0.010167148], [0.027895648, 0.014312723, 0.021143952], 
               [0.05831743, 0.019102171, 0.039416204], [0.008729752, 0.025987929, 0.017576094]]
    
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
        if std_dist < 6:
            return color_names[i]
            
    return None

def orient():
    if prev_color=='BLUE' or prev_color == None:
        MOTORR.set_power(-20)
        MOTORL.set_power(20)
        time.sleep(1)
        MOTORR.set_power(0)
        MOTORL.set_power(0)
    
    elif prev_color == 'RED':
        MOTORL.set_power(-20)
        MOTORR.set_power(20)
        time.sleep(0.5)
        MOTORR.set_power(0)
        MOTORL.set_power(0)
        
    MOTORR.set_power(20)
    MOTORL.set_power(20)
    time.sleep(0.75)
    MOTORR.set_power(0)
    MOTORL.set_power(0)
    time.sleep(2)
        
    
def find_zone():
    print("initiating finding zone sequence")
    rgb = SIDE_COLOR_SENSOR.get_rgb()
    color = side_check_color(rgb)
    
    if color == None: #swivel around backwards to find zone
        while color == None:
            print("Looking for zone")
            MOTORR.set_power(20)
            MOTORL.set_power(-15)
            time.sleep(0.25)
            rgb = SIDE_COLOR_SENSOR.get_rgb()
            color = side_check_color(rgb)

    print("found deliv zone color:"+ color)
    return color


def rotate_platform(zone_color):
    if zone_color=="RED":
        angle=0
    elif zone_color=="ORANGE":
        angle=60
    elif zone_color=="YELLOW":
        angle=120
    elif zone_color=="GREEN":
        angle=180
    elif zone_color=="BLUE":
        angle=240
    elif zone_color=="PURPLE":
        angle=300
    MOTORPLAT.reset_encoder()
    MOTORPLAT.set_limits(30)
    MOTORPLAT.set_position(angle)
    time.sleep(1.25)
    kick_block()
    time.sleep(1.15)
    MOTORPLAT.set_position(0)

# def test_rotate():
#     MOTORPLAT.set_limits(30)
#     MOTORPLAT.set_position(360)
#     time.sleep(1.15)
#     kick_block()
#     time.sleep(1.5)
#     MOTORPLAT.set_position(0)

def kick_block():
    reset_motor()
    MOTORKICK.set_limits(40)
    MOTORKICK.set_position(135)
    time.sleep(1)
    MOTORKICK.set_position(0)
    
def reset_motor(): 
    MOTORL.set_dps(0)
    MOTORL.set_dps(0)
    MOTORL.set_power(0)
    MOTORR.set_power(0)
    
def move_out_of_zone(zone_color):
    rgb = SIDE_COLOR_SENSOR.get_rgb()
    color = side_check_color(rgb)
    while color != None:
        MOTORR.set_power(10)
        MOTORL.set_power(10)
        time.sleep(0.4)
        rgb = SIDE_COLOR_SENSOR.get_rgb()
        color = side_check_color(rgb)
    MOTORR.set_power(0)
    MOTORL.set_power(0)
    print("out of zone!")
    MOTORPLAT.set_limits(20)
    rotate_platform(zone_color) # unloading mechanism
    time.sleep(1)

def go_back_on_track():
    print("looking for track")
    MOTORL.set_power(-20)
    MOTORR.set_power(20)
    
    rgb = COLOR_SENSOR.get_rgb()
    color = check_color(rgb)
    #if color == None: #swivel around backwards to find zone
    while True:
        rgb = COLOR_SENSOR.get_rgb()
        color = check_color(rgb)
        print(color)
        if color == "RED":
            MOTORL.set_power(-30)
            MOTORR.set_power(30)
            return
        elif color == "BLUE":
            prev_color=color
            print("blue")
            MOTORL.set_power(30)
            MOTORR.set_power(-30)
            return
#           print(color)
        #time.sleep(0.25)
    

# main entry point
try:
    blocks_delivered=0
    while blocks_delivered<6:
        # motor initialization
        print("initialzing motors\n")
        prev_color=None
        MOTORL.set_limits(POWER_LIMIT, SPEED_LIMIT)
        MOTORR.set_limits(POWER_LIMIT, SPEED_LIMIT)
        MOTORL.set_power(-20)
        MOTORR.set_power(20)
        MOTORKICK.reset_encoder()
        while blocks_delivered<6:
            rgb = COLOR_SENSOR.get_rgb()
            # print(rgb)
            color = check_color(rgb)
            #print(color)
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
                move_out_of_zone(zone_color)
                blocks_delivered+=1
                print("blocks delivered = " + str(blocks_delivered))
                go_back_on_track()

                # test_rotate()
                # #rotate_platform(color)
                # kick_block()
                # time.sleep(3)
                # MOTORL.set_position(90)
                # MOTORR.set_position(90)
                # continue
            else:
                MOTORL.set_power(20)
                MOTORR.set_power(20)
            
    #         if color!= None and color!="GREEN":
    #             prev_color=color
    #             print("HELLO"+ str(prev_color))
            #print("Blocks left: "+str((6-blocks_delivered)))
            time.sleep(0.1)
            # do smth with the rgb values
    print("going back to start")
    # go forward a bit
    MOTORL.set_power(20)
    MOTORR.set_power(20)
    time.sleep(1)
    print("doing 360")
    MOTORL.set_power(40)
    MOTORR.set_power(-40)
    time.sleep(2)
    while True:
        rgb = COLOR_SENSOR.get_rgb()
        # print(rgb)
        color = check_color(rgb)
        #print(color)
        if color == "RED":
            print("red")
            prev_color=color
            MOTORL.set_power(30)
            MOTORR.set_power(-30)
        elif color == "BLUE":
            prev_color=color
            print("blue")
        elif color == "YELLOW":
            MOTORL.set_power(0)
            MOTORR.set_power(0)
            
    
    
    

        
except KeyboardInterrupt:
    print("Ending by keyboard interrupt")
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()