from utils import sound
from utils.brick import BP, Motor, TouchSensor, EV3ColorSensor, wait_ready_sensors, reset_brick 
import time
import math

MOTORL = Motor("D") 
MOTORR = Motor("A")
MOTORPLAT = Motor("C")
MOTORKICK = Motor("B")
COLOR_SENSOR = EV3ColorSensor(4)
SIDE_COLOR_SENSOR = EV3ColorSensor(1)
TOUCH_SENSOR = TouchSensor(3)
SOUND = sound.Sound(duration=1, pitch="A4", volume=100)

POWER_LIMIT = 40
SPEED_LIMIT = 360

def side_check_color(rgb):
    means = [[0.98269282, 0.166543148, 0.079804332], [0.956722739, 0.279694185, 0.075963383], 
             [0.736488044, 0.672059319, 0.075039654], [0.313354802, 0.927045185, 0.202401399],
             [0.368746318, 0.608397841, 0.698980325], [0.963167792, 0.175536085, 0.201083857]]
    std_dev = [[0.004002433, 0.016609388, 0.01300176], [0.00668939, 0.023818665, 0.008397344],
               [0.00948927, 0.009867564, 0.010167148], [0.027895648, 0.014312723, 0.021143952], 
               [0.05831743, 0.019102171, 0.039416204], [0.018729752, 0.035987929, 0.027576094]]
    
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
        if std_dist < 5:
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

def orient(prev_color):
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
    #time.sleep(2)
        
    
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
        angle=70
    elif zone_color=="YELLOW":
        angle=120
    elif zone_color=="GREEN":
        angle=195
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

def kick_block():
    reset_motor()
    MOTORKICK.set_limits(35)
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
        MOTORR.set_power(15)
        MOTORL.set_power(15)
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
        if color == "RED":
            MOTORL.set_power(-30)
            MOTORR.set_power(30)
            return
        elif color == "BLUE":
            MOTORL.set_power(30)
            MOTORR.set_power(-30)
            return

def do_360(speed):
    print("doing 360")
    rgb = COLOR_SENSOR.get_rgb()
    color = check_color(rgb)
    while color != "BLUE":
        if color == "GREEN":
            print("green")
            rgb = COLOR_SENSOR.get_rgb()
            color = check_color(rgb)
            while color == "GREEN":
                rgb = COLOR_SENSOR.get_rgb()
                color = check_color(rgb)
                MOTORL.set_power(-1 * speed)
                MOTORR.set_power(speed)
                time.sleep(0.1)
            print("done green")
            return    
        #go_backwards(0.5)
        rgb = COLOR_SENSOR.get_rgb()
        color = check_color(rgb)
        MOTORL.set_power(-1 * speed)
        MOTORR.set_power(speed)
        time.sleep(0.1)
#     MOTORL.set_power(-30)
#     MOTORR.set_power(30)
#     time.sleep(4.5)
    MOTORL.set_power(0)
    MOTORR.set_power(0)

def return_to_loading():
    print("returning to loading zone")
    prev_color = "BLUE"
    while True:
        rgb = COLOR_SENSOR.get_rgb()
        color = check_color(rgb)
        if color == "RED":
            prev_color=color
            MOTORL.set_power(30)
            MOTORR.set_power(-30)
        elif color == "BLUE":
            prev_color=color
            MOTORL.set_power(-30)
            MOTORR.set_power(30)
        elif color == "GREEN":
            if prev_color == "RED":
                MOTORL.set_power(30)
                MOTORR.set_power(-5)
            elif prev_color == "BLUE":
                MOTORL.set_power(-5)
                MOTORR.set_power(30)
            #time.sleep(0.5)    
#             MOTORL.set_power(30)
#             MOTORR.set_power(30)
#             time.sleep(0.25)
        elif color == "YELLOW":
            print("found beginning")
            MOTORL.set_power(0)
            MOTORR.set_power(0)
            return
        else:
            MOTORL.set_power(30)
            MOTORR.set_power(30)
        time.sleep(0.1)

def deliver_blocks():
    blocks_delivered=0
    while blocks_delivered < 6:
        # motor initialization
        print("initialzing motors\n")
        prev_color = None
        MOTORL.set_limits(POWER_LIMIT, SPEED_LIMIT)
        MOTORR.set_limits(POWER_LIMIT, SPEED_LIMIT)
        MOTORL.set_power(-25)
        MOTORR.set_power(25)
        MOTORKICK.reset_encoder()
        while blocks_delivered < 6:
            rgb = COLOR_SENSOR.get_rgb()
            color = check_color(rgb)
            if color == "RED":
                prev_color = color
                MOTORL.set_power(-30)
                MOTORR.set_power(30)
            elif color == "BLUE":
                prev_color = color
                MOTORL.set_power(30)
                MOTORR.set_power(-30)
            elif color == "GREEN":
                reset_motor()
                time.sleep(0.25) #stop for a sec to emphasize sensing green
                # find the zone
                print("looking for zone")
                orient(prev_color) #function by matt
                zone_color = find_zone()
                move_out_of_zone(zone_color)
                blocks_delivered += 1
                print("blocks delivered = " + str(blocks_delivered))
                if blocks_delivered != 6:
                    go_back_on_track()
            else:
                MOTORL.set_power(25)
                MOTORR.set_power(25)
            time.sleep(0.1)
            
def turn_end(speed):
    print("turning at the end")
    # turn till you read blue
    rgb = COLOR_SENSOR.get_rgb()
    color = check_color(rgb)
    while color != "BLUE":
        rgb = COLOR_SENSOR.get_rgb()
        color = check_color(rgb)
        MOTORL.set_power(-1 * speed)
        MOTORR.set_power(speed)
        time.sleep(0.1)
        
    #go back
    MOTORL.set_power(-30)
    MOTORR.set_power(-10)
    time.sleep(1)
    
    # turn till it sees red
    rgb = COLOR_SENSOR.get_rgb()
    color = check_color(rgb)
    while color != "RED":
        rgb = COLOR_SENSOR.get_rgb()
        color = check_color(rgb)
        MOTORL.set_power(-1 * speed)
        MOTORR.set_power(speed)
        time.sleep(0.1)
        
    
def play_sound():
    SOUND.play()
    SOUND.wait_done()
    
def go_forward(t):
    MOTORL.set_power(25)
    MOTORR.set_power(25)
    time.sleep(t)
    
def go_backwards(t):
    MOTORL.set_power(-25)
    MOTORR.set_power(-25)
    time.sleep(t)
    

try:
    # set motor limits
    print("sensors initializing")
    wait_ready_sensors()
    print("done initializing")
    is_pressed = False
    while True:
        if TOUCH_SENSOR.is_pressed():
            # set button pressed to true
            is_pressed = True
            rgb = COLOR_SENSOR.get_rgb()
            
        if not TOUCH_SENSOR.is_pressed() and is_pressed == True:
            print("button pressed")
            is_pressed = False
            deliver_blocks()
            go_forward(1.5)
            turn_end(30)
            return_to_loading()
            fggo_forward(1.75)
            do_360(25)
            MOTORL.set_power(20)
            MOTORR.set_power(-20)
            time.sleep(1.5)
            go_backwards(1.5)
            reset_motor()
            play_sound()
        
except KeyboardInterrupt:
    print("Ending by keyboard interrupt")
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()