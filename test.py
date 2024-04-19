import os
import pygame
from pygame.locals import *
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Pygame and controller initialization
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Control table address
ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_CURRENT = 102
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132

# Data Byte Length
LEN_GOAL_CURRENT = 2
LEN_GOAL_POSITION = 4

# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL_ID = 7
BAUDRATE = 57600
DEVICENAME = '/dev/DYNAMIXEL'  # Check your port

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Operating Modes
CURRENT_CONTROL_MODE = 0
POSITION_CONTROL_MODE = 3

# Goal settings
goal_current_mA = 6  # in mA
goal_position_1 = 1800  # Example position

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if not portHandler.openPort():
    print("Failed to open the port!")
    quit()

# Set port baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baudrate!")
    quit()

def enable_torque(enable):
    return packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, enable)

def set_operating_mode(mode):
    enable_torque(TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    enable_torque(TORQUE_ENABLE)

def set_goal_current(current):
    packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, current)

def set_goal_position(position):
    packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)

if enable_torque(TORQUE_ENABLE)[0] != COMM_SUCCESS:
    print("Failed to enable torque!")
    quit()

print("Dynamixel has been successfully connected and controller is ready.")

try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == JOYBUTTONDOWN:
                if joystick.get_button(0):  # X button
                    set_operating_mode(CURRENT_CONTROL_MODE)
                    set_goal_current(goal_current_mA)
                    print(f"{goal_current_mA}mA current set.")
                elif joystick.get_button(1):  # Circle button
                    set_operating_mode(POSITION_CONTROL_MODE)
                    set_goal_position(goal_position_1)
                    print(f"Moving to position {goal_position_1}.")
            elif event.type == JOYAXISMOTION:
                if joystick.get_axis(1) < -0.5:  # Up on the left stick
                    goal_position_1 += 100
                    set_goal_position(goal_position_1)
                    print(f"Position increased to {goal_position_1}.")
                elif joystick.get_axis(1) > 0.5:  # Down on the left stick
                    goal_position_1 -= 100
                    set_goal_position(goal_position_1)
                    print(f"Position decreased to {goal_position_1}.")
            elif event.type == pygame.QUIT:
                running = False
finally:
    enable_torque(TORQUE_DISABLE)
    portHandler.closePort()
    pygame.quit()
