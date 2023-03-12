#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor
from time import sleep


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(2)
TOUCH_SENSOR = TouchSensor(1)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    print("Collect color sensor data.")

    # clear the contents of the file
    output_file = open(COLOR_SENSOR_DATA_FILE, "w").close()
 
    # loop to continously collect color data
    rgb = []
    is_pressed = False
    while True:
        if TOUCH_SENSOR.is_pressed():
            rgb = [0, 0, 0]
            # set button pressed to true
            is_pressed = True
            # verify valid entry
            
            while (rgb == [None, None, None] or rgb == [0, 0, 0]):
                rgb = COLOR_SENSOR.get_rgb()
            
        if not TOUCH_SENSOR.is_pressed() and is_pressed == True:
            # open the file
            output_file = open(COLOR_SENSOR_DATA_FILE, "a")
            # Collect the rgb values and print it to the terminal and file
            str_rgb = str(rgb)
            print("rgb values are:" + " " + str_rgb[1:-1])
            # output_file.write(f"{str_rgb}\n")
            # if we dont want it saved as a list, just comma seperated values 
            output_file.write(f"{str_rgb[1:-1]}\n")
            output_file.close()
            #set button pressed to false
            is_pressed = False
            sleep(0.06)


if __name__ == "__main__":
    collect_color_sensor_data()
