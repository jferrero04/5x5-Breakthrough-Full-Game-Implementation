from Game import *
from Robot373 import *


#
#
#  Define all the basic game functions
#
# 
left,right=Motors("ab")

def forward():
    left.power=17
    right.power=17

def stop():
    left.power=0
    right.power=0

def reverse():
    left.power=-17
    right.power=-17

def powermotorsleft():
    left.power=17
    right.power=-17

def powermotorsright():
    left.power=-17
    right.power=17

def degrees(position):
    return abs(position)*1.0

def distance_traveled(position):
    wheel_diameter_cm=7.62
    pi=3.141592653589793235
    return pi*wheel_diameter_cm*degrees(position)/360

def forward1():
    forward()
    Wait(1)
    stop()

    
#
#
#  MOVEMENT FUNCTIONS
#
#
def go_forward_squares_yellow(number_cols_to_move):  # THIS FUNCTION GETS TO FIRST YELLOW
    print("Yellow function started")
    distance_per_yellow_cm1=(7.56*2.54)*number_cols_to_move
    total_distance_cm1=distance_per_yellow_cm1
    left.reset_position()
    forward()
    print("Motor power set:",left.power,right.power)
    print("Starting forward movement")
    while distance_traveled(left.position)<total_distance_cm1:
        Wait(0.01)

def rot90():
    print("Rotate 90 started")
    left.reset_position()
    left.power=17
    right.power=-17
    axis_length_cm=16.5  # 6.69in axle to axle converted to 17 cm
    pi=3.14159
    distance_needed=(axis_length_cm/2)*2*pi/4  # need a quarter turn of the robot
    while distance_traveled(left.position)<distance_needed:
        Wait(0.01)

def go_forward_squares_blue(number_rows_to_move):   # THIS FUNCTION MOVES TO 1 SQUARE. Implement AFTER rot90() function
    print("Blue function started")
    distance_per_yellow_cm2=(5.75*2.54)*number_rows_to_move
    total_distance_cm2=distance_per_yellow_cm2
    left.reset_position()
    forward()
    print("Motor power set:",left.power,right.power)
    print("Starting forward movement")
    while distance_traveled(left.position)<total_distance_cm2:
        Wait(0.01)
    stop()

def diagonal_left():
    print("Starting diagonal capture left")    
    powermotorsleft()
    axis_length_cm=16.5 # 6.69in axle to axle so that equals 17cm
    pi=3.14159
    distance_needed=(axis_length_cm/2)*2*pi/4  # need half a quarter turn of the robot
    left.reset_position()
    while distance_traveled(left.position)<distance_needed:
        Wait(0.01)
    forward()
    Wait(1.25)
    stop()

def diagonal_right():
    print("Starting diagonal capture right")    
    powermotorsright()
    axis_length_cm=16.5 # 6.69in axle to axle so that equals 17cm
    pi=3.14159
    distance_needed=(axis_length_cm/2)*2*pi/4  # need half a quarter turn of the robot
    left.reset_position()
    while distance_traveled(left.position)<distance_needed:
        Wait(0.01)
    forward()
    Wait(1.25)
    stop()

def off_board():
    left.power=-17
    right.power=-17
    Wait(7)
    stop()
    
    
#
#
# Functions for Image Taking
#
#
def take_picture(filename='current_board.jpg',brightness=100,view=False,S=10):
    a=os.system(f"fswebcam -s brightness={brightness}%% -r 1600x900 --no-banner -S {S} '{filename}'")



