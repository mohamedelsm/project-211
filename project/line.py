from utils.brick import BP, Motor, TouchSensor, EV3ColorSensor, wait_ready_sensors, reset_brick 
import time

MOTORL = Motor("A") 
MOTORR = Motor("B")
COLOR_SENSOR = EV3ColorSensor(2)

POWER_LIMIT = 40
SPEED_LIMIT = 360

RW=0.028
RB=0.043
ORIENTTODEG = RB/RW
# set motor limits


def rotate(angle, speed):
    MOTORL.set_position_relative(angle * ORIENTTODEG)
    MOTORR.set_position_relative(-1 * angle * ORIENTTODEG)

# main entry point
try:
    # motor initialization
    print("initialzing motors")
    MOTORL.set_limits(POWER_LIMIT, SPEED_LIMIT)
    MOTORR.set_limits(POWER_LIMIT, SPEED_LIMIT)
    MOTORL.set_power(40)
    MOTORR.set_power(40)

    while True:
        rgb = COLOR_SENSOR.get_rgb() 
        print(rgb)
        # do smth with the rgb values
            
except KeyboardInterrupt:
    print("Ending by keyboard interrupt")
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()