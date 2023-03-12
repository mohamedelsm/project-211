from utils.brick import BP, Motor, TouchSensor, EV3ColorSensor, wait_ready_sensors, reset_brick 
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
        R=rgb[0]
        G=rgb[1]
        B=rgb[2]
        
        if R in range(110,190) and G in range(10,28) and B in range(10,16):
            print("red")
            MOTORL.set_power(-15)
            MOTORR.set_power(70)
        elif R in range(15,30) and G in range(15,30) and B in range(25,40):
            print("blue")
            MOTORL.set_power(70)
            MOTORR.set_power(-15)
        elif R in range(15,45) and G in range(40,75) and B in range(5,25):
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